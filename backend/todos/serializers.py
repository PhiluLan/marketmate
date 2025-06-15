from rest_framework import serializers
from .models import ToDo

class ToDoSerializer(serializers.ModelSerializer):
    # Automatisch wird das User-Feld in der API nicht übergeben, 
    # sondern wir setzen es im View anhand des angemeldeten Users.
    class Meta:
        model = ToDo
        fields = [
            'id',
            'user',
            'title',
            'description',
            'is_completed',
            'due_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
