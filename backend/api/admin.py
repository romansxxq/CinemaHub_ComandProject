from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Movie, Hall, Seat, Session, Booking

# Реєструємо нашу кастомну модель користувача
admin.site.register(User, UserAdmin)

# Реєструємо інші моделі
admin.site.register(Movie)
admin.site.register(Hall)
admin.site.register(Seat)
admin.site.register(Session)
admin.site.register(Booking)