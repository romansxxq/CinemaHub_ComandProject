from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Movie, Genre, Hall, Seat, Session, Booking, HallType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_url', 'duration', 'genres', 'is_now_showing')


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class HallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallType
        fields = ('id', 'name')


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ('id', 'row', 'number', 'is_vip')


class HallSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Hall
        fields = ('id', 'name', 'rows', 'seats_per_row', 'seats')


class SessionSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    hall_type_name = serializers.CharField(source='hall_type.name', read_only=True)
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = (
            'id', 'movie', 'movie_title', 'hall', 'hall_name', 
            'hall_type', 'hall_type_name', 'start_time', 'end_time',
            'base_price_standard', 'base_price_vip'
        )

    def get_end_time(self, obj):
        return obj.end_time


class SessionDetailSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    movie = MovieDetailSerializer(read_only=True)
    hall = HallSerializer(read_only=True)
    hall_type = HallTypeSerializer(read_only=True)
    end_time = serializers.SerializerMethodField()
    booked_seats = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = '__all__'

    def get_end_time(self, obj):
        return obj.end_time

    def get_booked_seats(self, obj):
        """Get list of booked seat IDs for this session"""
        booked = Booking.objects.filter(
            session=obj,
            status__in=['pending', 'paid']
        ).values_list('seat_id', flat=True)
        return list(booked)


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('session', 'seat', 'status')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie_title = serializers.CharField(source='session.movie.title', read_only=True)
    session_time = serializers.CharField(source='session.start_time', read_only=True)
    hall_name = serializers.CharField(source='session.hall.name', read_only=True)
    seat_info = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ('id', 'user', 'movie_title', 'session_time', 'hall_name', 'seat_info', 'status', 'created_at')

    def get_seat_info(self, obj):
        return f"Ряд {obj.seat.row}, Місце {obj.seat.number}"


class BookingDetailSerializer(serializers.ModelSerializer):
    session = SessionDetailSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
