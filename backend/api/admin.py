import requests
from datetime import datetime
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from .models import User, HallType, Movie, Hall, Seat, Session, Booking

admin.site.register(User, UserAdmin)


@admin.register(HallType)
class HallTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class MovieAdminForm(forms.ModelForm):
    fetch_from_omdb = forms.BooleanField(
        required=False,
        initial=True,
        label='Auto-fill from IMDb (OMDb)',
        help_text='If enabled, the admin will try to fetch and fill fields using IMDb ID or Title.'
    )

    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm
    list_display = ('title', 'duration', 'imdb_id', 'is_now_showing', 'release_date', 'created_at')
    list_filter = ('is_now_showing', 'release_date', 'created_at')
    search_fields = ('title', 'imdb_id')
    
    def save_model(self, request, obj, form, change):
        api_key = "fe50d514"
        data = None
        omdb_genres_raw = None

        fetch_from_omdb = False
        if hasattr(form, 'cleaned_data'):
            fetch_from_omdb = bool(form.cleaned_data.get('fetch_from_omdb'))
        
        if fetch_from_omdb:
            # ВАРІАНТ 1: Адмін ввів IMDb ID (точний пошук)
            if obj.imdb_id and not obj.description:
                url = f"http://www.omdbapi.com/?apikey={api_key}&i={obj.imdb_id}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

            # ВАРІАНТ 2: Адмін ввів лише НАЗВУ (пошук по тексту)
            elif obj.title and not obj.imdb_id:
                # Замість параметра 'i' використовуємо 't' (Title)
                url = f"http://www.omdbapi.com/?apikey={api_key}&t={obj.title}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
        else:
            # If user opted out of auto-fetch, do not call OMDb
            if obj.imdb_id or obj.title:
                messages.info(request, "Saved manually (auto-fill from IMDb/OMDb is disabled).")

        # Якщо API повернуло дані (успішний пошук хоч за ID, хоч за назвою)
        if data and data.get("Response") == "True":
            # Заповнюємо/оновлюємо поля
            obj.title = data.get('Title', obj.title)
            obj.imdb_id = data.get('imdbID') or obj.imdb_id
            obj.description = data.get('Plot', '')

            imdb_rating = data.get('imdbRating')
            try:
                obj.rating = float(imdb_rating) if imdb_rating and imdb_rating != 'N/A' else None
            except (TypeError, ValueError):
                obj.rating = None

            released = data.get('Released')
            if released and released != 'N/A' and not obj.release_date:
                try:
                    obj.release_date = datetime.strptime(released, '%d %b %Y').date()
                except ValueError:
                    pass
            
            runtime_str = data.get('Runtime', '0 min')
            try:
                obj.duration = int(runtime_str.split()[0])
            except ValueError:
                obj.duration = 0
                
            poster = data.get('Poster')
            if poster and poster != "N/A":
                obj.poster_url = poster

            # Genres from OMDb come as a comma-separated string, e.g. "Action, Drama"
            omdb_genres = data.get('Genre')
            if omdb_genres and omdb_genres != 'N/A':
                omdb_genres_raw = omdb_genres
        elif fetch_from_omdb and (obj.imdb_id or obj.title):
            messages.warning(request, "Could not fetch data from OMDb (check IMDb ID/title or API availability). Saved with provided values.")

        # Normalize imdb_id: avoid saving empty string which breaks UNIQUE in SQLite
        if not obj.imdb_id or obj.imdb_id == 'N/A':
            obj.imdb_id = None

        # If admin tries to add a movie with an existing imdb_id, update the existing record
        if not change and obj.imdb_id:
            existing = Movie.objects.filter(imdb_id=obj.imdb_id).first()
            if existing:
                obj.pk = existing.pk
                messages.info(request, f"Movie with IMDb ID {obj.imdb_id} already exists — updated it instead of creating a duplicate.")

        super().save_model(request, obj, form, change)

        # Store OMDb genres as simple text on Movie
        if fetch_from_omdb and omdb_genres_raw:
            Movie.objects.filter(pk=obj.pk).update(genres_text=omdb_genres_raw)

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'rows', 'seats_per_row')

# Кастомні дії для швидкого керування VIP статусом
@admin.action(description="Зробити обрані місця VIP (Золотими)")
def make_vip(modeladmin, request, queryset):
    # Оновлює всі обрані записи одним швидким запитом до БД
    queryset.update(is_vip=True)

@admin.action(description="Зняти статус VIP з обраних місць")
def remove_vip(modeladmin, request, queryset):
    queryset.update(is_vip=False)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('hall', 'row', 'number', 'is_vip')
    list_filter = ('hall', 'is_vip') # Фільтри збоку екрана
    list_editable = ('is_vip',)      # Дозволяє клікати галочки прямо у списку
    ordering = ('hall', 'row', 'number')
    actions = [make_vip, remove_vip] # Додаємо наші кастомні кнопки в меню "Дії"


# --- БАЗОВА АДМІНКА ДЛЯ СЕАНСІВ ТА БРОНЮВАНЬ ---
# (Щоб теж виглядало красиво, а не просто як `Object (1)`)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'hall_type', 'start_time', 'end_time', 'base_price')
    list_filter = ('movie', 'hall', 'hall_type', 'start_time')
    search_fields = ('movie__title', 'hall__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__email', 'session__movie__title')