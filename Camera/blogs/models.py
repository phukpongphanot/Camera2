from django.db import models

# Create your models here.
class Post(models.Model):
    IDCode = models.CharField(max_length = 11)
    content = models.TextField()   #ใส่ได้กี่ตัวอัษรก็ได้
    print("sss11ss")
    
