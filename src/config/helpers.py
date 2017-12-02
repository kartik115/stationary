from rest_framework.exceptions import PermissionDenied

def is_superuser(superuser):
	if superuser:
		return True
	else:
		raise PermissionDenied("only superuser has such rights")

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]