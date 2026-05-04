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


class HallType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Фільм
class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Name film", blank=True)
    description = models.TextField(verbose_name="Description", blank=True)
    poster_url = models.URLField(verbose_name="Poster URL", blank=True, null=True)
    trailer_url = models.URLField(verbose_name="Trailer URL", blank=True, null=True)
    duration = models.PositiveIntegerField(verbose_name="Duration (minutes)", blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    genres_text = models.TextField(blank=True, default='')
    is_now_showing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    release_date = models.DateField(null=True, blank=True)
    
    imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="IMDb ID")
    
    def __str__(self):
        return self.title

# Зал
class Hall(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name of the hall")
    rows = models.PositiveIntegerField(default=10, verbose_name="Count of rows")
    seats_per_row = models.PositiveIntegerField(default=15, verbose_name="Seats per row")
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Перевіряємо, чи це створення НОВОГО залу (якщо pk == None)
        is_new = self.pk is None 
        
        # Спочатку зберігаємо сам зал, щоб він отримав свій id (pk)
        super().save(*args, **kwargs)

        # Якщо зал щойно створено, генеруємо місця
        if is_new:
            seats_to_create = []
            
            for row in range(1, self.rows + 1):
                for number in range(1, self.seats_per_row + 1):
                    # Фішка: можемо зробити останній ряд автоматично VIP
                    is_vip = (row == self.rows)
                    
                    seats_to_create.append(
                        Seat(hall=self, row=row, number=number, is_vip=is_vip)
                    )
            
            Seat.objects.bulk_create(seats_to_create)
# Місце в залі
class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField(verbose_name="Row")
    number = models.PositiveIntegerField(verbose_name="Seat Number")
    is_vip = models.BooleanField(default=False, verbose_name="VIP Seat")

    @property
    def seat_type(self):
        return 'vip' if self.is_vip else 'standard'

    class Meta:
        unique_together = ('hall', 'row', 'number')

    def __str__(self):
        return f"{self.hall.name} - Ряд {self.row}, Місце {self.number}"

# Сеанс
class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='sessions')
    hall_type = models.ForeignKey(HallType, on_delete=models.CASCADE, null=True, blank=True, related_name='sessions')
    start_time = models.DateTimeField(verbose_name="Час початку")
    base_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Базова ціна")
    base_price_standard = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    base_price_vip = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

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
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")

    class Meta:
        # Запобігає Double Booking на рівні бази даних
        unique_together = ('session', 'seat')

    def __str__(self):
        return f"Ticket {self.id} - {self.user.email} - {self.status}"