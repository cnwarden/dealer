from django.db import models

# Create your models here.
class stock_record(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __unicode():
        return u'%s' % (code)
