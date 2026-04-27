from django.db import IntegrityError, transaction
from rest_framework import serializers

from ..models import User


class RegistrationError(Exception):
    pass


def register_user(validated_data):
    """Create a user inside a transaction.

    Expects validated_data dict from UserRegisterSerializer.
    Returns created User or raises RegistrationError/serializers.ValidationError.
    """
    # Copy relevant fields
    data = {
        'email': validated_data.get('email'),
        'username': validated_data.get('username'),
        'first_name': validated_data.get('first_name', ''),
        'last_name': validated_data.get('last_name', ''),
    }
    password = validated_data.get('password')

    if not password:
        raise serializers.ValidationError({'password': 'Password is required.'})

    try:
        with transaction.atomic():
            user = User(**data)
            user.set_password(password)
            user.save()
            return user
    except IntegrityError as e:
        # Map DB integrity issues to readable errors
        msg = str(e)
        # Simple parsing for unique constraint messages
        if 'email' in msg.lower():
            raise serializers.ValidationError({'email': 'A user with this email already exists.'})
        if 'username' in msg.lower():
            raise serializers.ValidationError({'username': 'A user with this username already exists.'})
        raise RegistrationError(msg)
