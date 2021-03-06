from rest_framework import serializers
from .models import Event, Contract, Customer, Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'role']
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True}}

    def create_user(self, email, password, role, first_name=None, last_name=None):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = Users.objects.create(
            email=email,
            role=role
        )
        if first_name and isinstance(first_name, str):
            user.first_name = first_name
        else:
            user.first_name = ""
        if last_name and isinstance(last_name, str):
            user.last_name = last_name
        else:
            user.last_name = ""
        user.set_password(password)
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'id', 'sales', 'first_name', 'last_name', 'email',
            'mobile', 'company_name', 'date_creation', 'date_update'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'date_creation': {'read_only': True},
            'date_update': {'read_only': True},
            'sales': {'read_only': True},
        }


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'customer', 'sales', 'value', 'status', 'time_created']
        extra_kwargs = {
            'id': {'read_only': True},
            'sales': {'read_only': True},
            'time_created': {'read_only': True},
        }


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'contract', 'title', 'date', 'support', 'status', 'time_created']
        extra_kwargs = {
            'id': {'read_only': True},
            'time_created': {'read_only': True}
        }
