from django.db import models
from django.contrib.auth.models import User

from config.models import TimeStampedModel

# Create your models here.


class Hardware(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    serialcode = models.CharField(max_length=30, null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=False)
    cost = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = "hardware"


class TrackHardware(TimeStampedModel):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, models.DO_NOTHING)
	hardware = models.ForeignKey(Hardware, models.DO_NOTHING)
	start_date = models.DateField(null=False, blank=False)
	end_date = models.DateField(null=True, blank=True)

	class Meta:
		db_table = "track_hardware"
		unique_together = ('user','hardware','start_date')


class RepairHardware(TimeStampedModel):
	id = models.AutoField(primary_key=True)
	track = models.ForeignKey(TrackHardware, models.DO_NOTHING)
	repair_cost = models.IntegerField()

	class Meta:
		db_table = "repair_hardware"