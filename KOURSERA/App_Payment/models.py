from django.db import models
from django.conf import settings

class BillingAddress(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.CharField(max_length=264,blank=True)
    zipcode = models.CharField(max_length=30,blank=True)
    city    = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return str(self.user) + " Address"

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self,field_name)
            if value is None or value=="":
                return False

        return True 


    class Meta:
        verbose_name_plural = "Billing Address"
        
         
