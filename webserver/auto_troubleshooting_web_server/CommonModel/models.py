from django.db import models

# Create your models here.

class AccessLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=2048)


    def __str__(self):
        return f"{self.url} - {self.ip}"