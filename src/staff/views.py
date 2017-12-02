from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.db.models import F, Sum, Case, When
from django.contrib.auth.models import User
from django.db import connection

from .serializers import *
import config.helpers as helpers
import staff.methods as methods

# Create your views here.
    
@api_view(['POST','GET','PUT'])
def staff_user(request, user_id):
	if request.method == 'GET':
		response = methods.get_user(user_id)
	elif request.method == 'POST':
		#check superuser
		helpers.is_superuser(request.user.is_superuser)
		response = methods.add_user(user_id, request.data)
	elif request.method == 'PUT':
		#check superuser
		helpers.is_superuser(request.user.is_superuser)
		response = methods.edit_user(user_id, request.data)
	return Response(status=status.HTTP_200_OK, data=response)


@api_view(['GET','POST','PUT'])
def hardware(request, hardware_id=None):
	if request.method == 'GET':
		response = methods.get_hardware(hardware_id)
	elif request.method == 'POST':
		#check superuser
		helpers.is_superuser(request.user.is_superuser)
		response = methods.add_hardware(hardware_id, request.data)
	elif request.method == 'PUT':
		#check superuser
		helpers.is_superuser(request.user.is_superuser)
		response = methods.edit_hardware(hardware_id, request.data)
	return Response(status=status.HTTP_200_OK, data=response)


@api_view(['GET','POST','PUT'])
def hardware_track_history(request, track_id=None):
	if request.method == 'GET':
		response = methods.get_hardware_track_history(track_id, request)
	elif request.method == 'POST':
		#check superuser
		helpers.is_superuser(request.user.is_superuser)
		if track_id is not None:
			raise ValidationError("Might be you are looking for PUT request")
		response = methods.add_hardware_track_history(track_id, request.data)
	elif request.method == 'PUT':
		#check superuser
		helpers.is_superuser(request.user.is_superuser)
		response = methods.edit_hardware_track_history(track_id, request.data)
	return Response(status=status.HTTP_200_OK, data=response)


@api_view(['POST','GET','PUT'])
def repair_history(request, repair_id=None):
	
	if request.method == 'GET':
		response = methods.get_repair_history(repair_id)
	
	elif request.method == 'POST':
		#check superuser
		helpers.is_superuser(request.user.is_superuser)
		response = methods.add_repair_history(repair_id, request.data)
	
	elif request.method == 'PUT':
		#check superuser
		helpers.is_superuser(request.user.is_superuser)
		response = methods.edit_repair_history(repair_id, request.data)
	
	return Response(status=status.HTTP_200_OK, data=response)


@api_view(['GET'])
def best_employee(request):
	sql = """SELECT u.id, u.username, u.first_name, u.last_name,
			case when sum(r.repair_cost) is null then 0 
				else sum(r.repair_cost) end as repair
			FROM stationary.auth_user as u
			left join stationary.track_hardware as t on t.user_id=u.id
			left join stationary.repair_hardware as r on r.track_id = t.id
			group by u.id
			order by repair asc, id asc limit 1;"""
	cursor = connection.cursor()
	cursor.execute(sql)
	response = helpers.dictfetchall(cursor)
	cursor.close()
	
	return Response(status=status.HTTP_200_OK, data=response)