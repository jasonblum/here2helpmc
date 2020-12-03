from django.db import models


class ExtraDelivery(models.Model):
    date = models.DateField()
    text = models.TextField()
    notes = models.TextField(null=True, blank=True)

class CancelledDelivery(models.Model):
    date = models.DateField()
    text = models.TextField()
    notes = models.TextField(null=True, blank=True)

