from django.db import models
from django.contrib.auth.models import User
import os


class Protocol(models.Model):
    name = models.CharField(max_length=100, blank=False)  # TODO: add validation for correct protocol
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='protocol', null=False)

    def __str__(self):
        return self.name

    def serialize(self):
        return self.name  # TODO: serialize self.dose_set

    @staticmethod
    def to_file(protocol, filename):
        os.path.dirname(filename)
        doses = ProtocolDose.objects.filter(protocol=protocol)
        with open(filename, 'w') as out:
            for dose in doses:
                out.write(str(dose.dose) + ' ')
            out.write('\n')
            for dose in doses:
                out.write(str(dose.time) + ' ')


class ProtocolDose(models.Model):
    protocol = models.ForeignKey(to='Protocol', on_delete=models.CASCADE, related_name='dose', null=False)
    time = models.IntegerField(verbose_name='Time of dose', null=False)
    dose = models.DecimalField(verbose_name='Dose', null=False, decimal_places=2, max_digits=4)

    class Meta:
        verbose_name = 'Protocol Dose'
