from django.db import models
<<<<<<< Updated upstream

# Create your models here.
=======
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="email adress")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# Жанр
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Жанр")
    
    def __str__(self):
        return self.name


# Фільм
class Movie(models.Model):
    RATING_CHOICES = [
        ('G', 'General Audiences (G)'),
        ('PG', 'Parental Guidance (PG)'),
        ('PG-13', 'Parents Strongly Cautioned (PG-13)'),
        ('R', 'Restricted (R)'),
        ('NC-17', 'No Children 17 or Younger (NC-17)'),
    ]

    title = models.CharField(max_length=255, verbose_name="Name film", blank=True)
    description = models.TextField(verbose_name="Description", blank=True)
    poster_url = models.URLField(verbose_name="Poster URL", blank=True, null=True)
    trailer_url = models.URLField(verbose_name="Trailer URL", blank=True, null=True)
    duration = models.PositiveIntegerField(verbose_name="Duration (minutes)", blank=True, null=True)
    
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default='PG-13', verbose_name="Age Rating")
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name="Genres")
    
    director = models.CharField(max_length=255, blank=True, verbose_name="Director")
    actors = models.TextField(blank=True, verbose_name="Actors (comma-separated)")
    
    release_date = models.DateField(null=True, blank=True, verbose_name="Release Date")
    is_now_showing = models.BooleanField(default=True, verbose_name="Now Showing")
    
    imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="IMDb ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


# Зал
class Hall(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name of the hall")
    rows = models.PositiveIntegerField(verbose_name="Number of rows", default=10)
    seats_per_row = models.PositiveIntegerField(verbose_name="Seats per row", default=15)
    
    def __str__(self):
        return self.name


# Місце в залі
class Seat(models.Model):
    SEAT_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('vip', 'VIP'),
    ]
    
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField(verbose_name="Row")
    number = models.PositiveIntegerField(verbose_name="Seat Number")
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES, default='standard', verbose_name="Seat Type")

    class Meta:
        unique_together = ('hall', 'row', 'number')
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.hall.name} - Ряд {self.row}, Місце {self.number}"


# Тип залу (2D, 3D, IMAX)
class HallType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Hall Type")
    
    def __str__(self):
        return self.name


# Сеанс
class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='sessions')
    hall_type = models.ForeignKey(HallType, on_delete=models.SET_NULL, null=True, verbose_name="Hall Type (2D, 3D, IMAX)")
    
    start_time = models.DateTimeField(verbose_name="Час початку")
    base_price_standard = models.DecimalField(max_digits=8, decimal_places=2, default=100, verbose_name="Standard Seat Price")
    base_price_vip = models.DecimalField(max_digits=8, decimal_places=2, default=150, verbose_name="VIP Seat Price")

    @property
    def end_time(self):
        """Автоматично вираховує час закінчення сеансу на основі тривалості фільму."""
        if self.movie and self.start_time and self.movie.duration:
            return self.start_time + timedelta(minutes=self.movie.duration)
        return None

    def __str__(self):
        return f"{self.movie.title} ({self.start_time.strftime('%d.%m %H:%M')})"
    
    class Meta:
        ordering = ['start_time']


# Бронювання
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
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ticket Price")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Запобігає Double Booking на рівні бази даних
        unique_together = ('session', 'seat')
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket {self.id} - {self.user.email} - {self.status}"
    
    def save(self, *args, **kwargs):
        # Validate that the seat is not already booked for this session
        if Booking.objects.filter(
            session=self.session, 
            seat=self.seat, 
            status__in=['pending', 'paid']
        ).exclude(pk=self.pk).exists():
            raise ValidationError("This seat is already booked for this session.")
        super().save(*args, **kwargs)
>>>>>>> Stashed changes
