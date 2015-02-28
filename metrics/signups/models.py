from django.db import models


class Signup(models.Model):
    signup_date = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.signup_date

