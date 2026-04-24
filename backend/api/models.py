import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="email adress")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# 2. Фільм
class Movie(models.fields.Model):
    title = models.CharField(max_length=255, verbose_name="Name film")
    description = models.TextField(verbose_name="Description", blank=True)
    poster_url = models.URLField(verbose_name="Poster URL", blank=True, null=True)
    duration = models.PositiveIntegerField(verbose_name="Duration (minutes)")
    
    # Поля для інтеграції з зовнішнім API (як ми обговорювали)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True, verbose_name="ID в TMDB")
    
    def __str__(self):
        return self.title

# 3. Зал
class Hall(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name of the hall (e.g., Red Hall)")
    
    def __str__(self):
        return self.name

# 4. Місце в залі
class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField(verbose_name="Row")
    number = models.PositiveIntegerField(verbose_name="Seat Number")
    is_vip = models.BooleanField(default=False, verbose_name="VIP Seat")

    class Meta:
        unique_together = ('hall', 'row', 'number')

    def __str__(self):
        return f"{self.hall.name} - Ряд {self.row}, Місце {self.number}"

# 5. Сеанс
class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField(verbose_name="Час початку")
    base_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Базова ціна")

    @property
    def end_time(self):
        """Автоматично вираховує час закінчення сеансу на основі тривалості фільму."""
        if self.movie and self.start_time:
            return self.start_time + timedelta(minutes=self.movie.duration)
        return None

    def __str__(self):
        return f"{self.movie.title} ({self.start_time.strftime('%d.%m %H:%M')})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує оплати'),
        ('paid', 'Оплачено'),
        ('cancelled', 'Скасовано'),
    ]

    # Використовуємо UUID для унікального ідентифікатора квитка (зручно для QR-коду)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")

    class Meta:
        # Запобігає Double Booking на рівні бази даних
        unique_together = ('session', 'seat')

    def __str__(self):
        return f"Квиток {self.id} - {self.user.email} - {self.status}"