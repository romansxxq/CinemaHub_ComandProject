from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


# The rest of the serializers are simple placeholders so imports succeed.
class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class MovieListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()


class MovieDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()


class HallTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class SeatSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    row = serializers.IntegerField()
    number = serializers.IntegerField()
    seat_type = serializers.CharField()


class HallSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class SessionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    movie = serializers.IntegerField()


class SessionDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)


class BookingCreateSerializer(serializers.Serializer):
    session = serializers.IntegerField()
    seat = serializers.IntegerField()


class BookingListSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)


class BookingDetailSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
