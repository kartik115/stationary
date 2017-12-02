from config.serializers import TimeStampedModelSerializer
from .models import *
from rest_framework import serializers


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_superuser', 'first_name', 'last_name')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class HardwareSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Hardware
        fields = ('id', 'serialcode', 'name', 
        	'cost') + TimeStampedModelSerializer.Meta.fields


class TrackHardwareSerializer(TimeStampedModelSerializer):
	class Meta:
		model=TrackHardware
		fields = ('id', 'hardware', 'user', 'start_date', 
			'end_date') + TimeStampedModelSerializer.Meta.fields


class RepairHardwareSerializer(TimeStampedModelSerializer):
	class Meta:
		model = RepairHardware
		fields = ('id', 'track', 'repair_cost') + TimeStampedModelSerializer.Meta.fields
