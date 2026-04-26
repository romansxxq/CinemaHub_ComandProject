import requests
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Movie, Hall, Seat, Session, Booking

admin.site.register(User, UserAdmin)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'imdb_id')
    
    def save_model(self, request, obj, form, change):
        api_key = "fe50d514" # Не забудьте вставити ваш ключ!
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