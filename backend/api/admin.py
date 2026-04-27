import requests
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Movie, Hall, Seat, Session, Booking

admin.site.register(User, UserAdmin)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'imdb_id')
    
    def save_model(self, request, obj, form, change):
        api_key = "fe50d514"
        data = None
        
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

        # Якщо API повернуло дані (успішний пошук хоч за ID, хоч за назвою)
        if data and data.get("Response") == "True":
            # Заповнюємо/оновлюємо поля
            obj.title = data.get('Title', obj.title)
            obj.imdb_id = data.get('imdbID', '') # Зберігаємо знайдений ID
            obj.description = data.get('Plot', '')
            
            runtime_str = data.get('Runtime', '0 min')
            try:
                obj.duration = int(runtime_str.split()[0])
            except ValueError:
                obj.duration = 0
                
            poster = data.get('Poster')
            if poster and poster != "N/A":
                obj.poster_url = poster

        super().save_model(request, obj, form, change)

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
    list_display = ('movie', 'hall', 'start_time', 'base_price')
    list_filter = ('movie', 'hall', 'start_time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session', 'status', 'created_at')
    list_filter = ('status',)
