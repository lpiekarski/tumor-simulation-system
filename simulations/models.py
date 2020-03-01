from django.db import models
from django.contrib.auth.models import User


class InitialTumor(models.Model):
    name = models.CharField(max_length=100, blank=False)
    file = models.FileField(upload_to='tumors/')  # TODO: add validation check for correct tumor file

    class Meta:
        verbose_name = 'Initial Tumor'

    def __str__(self):
        return self.name


class Protocol(models.Model):
    name = models.CharField(max_length=100, blank=False)  # TODO: add validation for correct protocol
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='protocol', null=False)

    def __str__(self):
        return self.name

    def serialize(self):
        return self.name  # TODO: serialize self.dose_set


class ProtocolDose(models.Model):
    protocol = models.ForeignKey(to='Protocol', on_delete=models.CASCADE, related_name='dose', null=False)
    time = models.IntegerField(verbose_name='Time of dose', null=False)
    dose = models.DecimalField(verbose_name='Dose', null=False, decimal_places=2, max_digits=4)

    class Meta:
        verbose_name = 'Protocol Dose'
