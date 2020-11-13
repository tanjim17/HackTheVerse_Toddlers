from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    doctorID = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Nurse(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nurseID = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Reception(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    receptionID = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Bed(models.Model):
    doctor_fk = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, null=True)
    nurse_fk = models.ForeignKey(Nurse, on_delete=models.DO_NOTHING, null=True)

    bedID = models.IntegerField(unique=True)
    floor = models.IntegerField()
    roomNo = models.IntegerField()

    def __str__(self):
        return 'Bed : ' + str(self.bedID)
