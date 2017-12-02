from django.contrib.auth.models import User
from .serializers import *
from django.db.models import F

def add_user(user_id, data):
	if user_id is not None:
		raise ValidationError("Might be you are looking for PUT request")
	user_serializer = UserSerializer(data=data)
	user_serializer.is_valid(raise_exception=True)
	user_serializer.save()
	response = user_serializer.data
	del response['password']
	return response

def edit_user(user_id, data):
	user = User.objects.filter(pk=user_id).first()
	user_serializer = UserSerializer(instance=user, data=data, partial=True)
	user_serializer.is_valid(raise_exception=True)
	user_serializer.save()
	response = user_serializer.data
	del response['password']
	return response

def get_user(user_id):
	if user_id is not None:
		response = TrackHardware.objects.filter(user_id=user_id)\
		.annotate(
			hardware_name=F('hardware__name'),
			hardware_serialcode=F('hardware__serialcode'),
			username=F('user__username'),
			firstname=F('user__first_name'),
			lastname=F('user__last_name')
			)\
		.values('id', 'hardware_id', 'hardware_name','user_id', 'username', 
			'start_date', 'firstname', 'lastname', 'hardware_serialcode')
	else:
		response = User.objects.values()
	return response


def get_hardware_track_history(track_id, request):
	response = TrackHardware.objects
	if track_id is not None:
		response = response.filter(pk=track_id).\
		values('id','hardware__name', 'user__username', 'hardware_id', 'user_id').first()
	else:
		if 'user_id' in request.GET:
			response = response.filter(user_id=request.GET.get('user_id'))
		if 'hardware_id' in request.GET:
			response = response.filter(hardware_id=request.GET.get('hardware_id'))
		if 'hardware_name' in request.GET:
			response = response.filter(hardware__name__startswith=request.GET.get('hardware_name'))
		if 'user_name' in request.GET:
			response = response.filter(user__username=request.GET.get('user_name'))
		response = response.\
		values('id','hardware__name', 'user__username', 'hardware_id', 'user_id')
	return response


def add_hardware_track_history(track_id, data):
	if track_id is not None:
		raise ValidationError("Might be you are looking for PUT request")
	track_serializer = TrackHardwareSerializer(data=data)
	track_serializer.is_valid(raise_exception=True)
	track_serializer.save()
	response = track_serializer.data
	return response


def edit_hardware_track_history(track_id, data):
	hardware_track = TrackHardware.objects.filter(pk=track_id).first()
	track_serializer = TrackHardwareSerializer(instance=hardware_track, 
											   data=data, partial=True)
	track_serializer.is_valid(raise_exception=True)
	track_serializer.save()
	response = track_serializer.data
	return response


def get_repair_history(repair_id):
	if repair_id is not None:
		response = RepairHardware.objects.filter(pk=repair_id)\
		.annotate(
			hardware_id=F('track__hardware_id'),
			hardware_name=F('track__hardware__name'),
			user_id=F('track__user_id'),
			username=F('track__user__username')
			)\
		.values('id','hardware_id','hardware_name','user_id', 'username').first()
	else:
		response = RepairHardware.objects.annotate(
			hardware_id=F('track__hardware_id'),
			hardware_name=F('track__hardware__name'),
			user_id=F('track__user_id'),
			username=F('track__user__username')
			)\
		.values('id','hardware_id','hardware_name','user_id', 'username')
	return response


def add_repair_history(repair_id, data):
	if repair_id is not None:
		raise ValidationError("Might be you are looking for PUT request")
	repair_serializer = RepairHardwareSerializer(data=data)
	repair_serializer.is_valid(raise_exception=True)
	repair_serializer.save()
	response = repair_serializer.data
	return response


def edit_repair_history(repair_id, data):
	repair_hardware = RepairHardware.objects.filter(pk=repair_id).first()
	repair_serializer = RepairHardwareSerializer(instance=repair_hardware, 
											     data=data, partial=True)
	repair_serializer.is_valid(raise_exception=True)
	repair_serializer.save()
	response = repair_serializer.data
	return response


def get_hardware(hardware_id):
	if hardware_id is not None:
		response = Hardware.objects.filter(pk=hardware_id).values().first()
	else:
		response = Hardware.objects.values()
	return response


def add_hardware(hardware_id, data):
	if hardware_id is not None:
		raise ValidationError("Might be you are looking for PUT request")
	hardware_serializer = HardwareSerializer(data=data)
	hardware_serializer.is_valid(raise_exception=True)
	hardware_serializer.save()
	response = hardware_serializer.data
	return response


def edit_hardware(hardware_id, data):
	hardware = Hardware.objects.filter(pk=hardware_id).first()
	hardware_serializer = HardwareSerializer(instance=hardware, data=data, partial=True)
	hardware_serializer.is_valid(raise_exception=True)
	hardware_serializer.save()
	response = hardware_serializer.data
	return response