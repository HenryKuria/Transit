from django.db import models


class Payment(models.Model):
    telephone = models.IntegerField()
    code = models.CharField(max_length=15, blank=True, null=True, auto_created=True)
    amount = models.IntegerField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.code)
