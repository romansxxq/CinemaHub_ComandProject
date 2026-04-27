from django.contrib import admin
<<<<<<< Updated upstream

# Register your models here.
=======
from .models import User, Genre, Movie, Hall, Seat, HallType, Session, Booking


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'rating', 'is_now_showing', 'release_date')
    list_filter = ('rating', 'is_now_showing', 'release_date')
    search_fields = ('title', 'description', 'director')
    filter_horizontal = ('genres',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'duration', 'rating')
        }),
        ('Media', {
            'fields': ('poster_url', 'trailer_url')
        }),
        ('Details', {
            'fields': ('director', 'actors', 'release_date', 'genres')
        }),
        ('External IDs', {
            'fields': ('imdb_id',)
        }),
        ('Status', {
            'fields': ('is_now_showing',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HallType)
class HallTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'rows', 'seats_per_row', 'total_seats')
    readonly_fields = ('total_seats',)

    def total_seats(self, obj):
        return obj.rows * obj.seats_per_row
    total_seats.short_description = 'Total Seats'


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('hall', 'row', 'number', 'seat_type')
    list_filter = ('hall', 'seat_type', 'row')
    search_fields = ('hall__name',)
    ordering = ('hall', 'row', 'number')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'hall_type', 'start_time', 'end_time', 'base_price_standard')
    list_filter = ('hall', 'hall_type', 'start_time', 'movie')
    search_fields = ('movie__title', 'hall__name')
    readonly_fields = ('end_time',)
    fieldsets = (
        ('Session Details', {
            'fields': ('movie', 'hall', 'hall_type', 'start_time', 'end_time')
        }),
        ('Pricing', {
            'fields': ('base_price_standard', 'base_price_vip')
        }),
    )
    ordering = ('-start_time',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session', 'seat', 'status', 'price', 'created_at')
    list_filter = ('status', 'created_at', 'session')
    search_fields = ('user__email', 'session__movie__title', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Booking Information', {
            'fields': ('id', 'user', 'session', 'seat')
        }),
        ('Payment', {
            'fields': ('status', 'price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
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

admin.site.register(Hall)
admin.site.register(Seat)
admin.site.register(Session)
admin.site.register(Booking)
>>>>>>> Stashed changes
