from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Producto


class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Producto
        fields = [
            "url",
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "fecha_creacion",
            "fecha_actualizacion",
            "activo"
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
