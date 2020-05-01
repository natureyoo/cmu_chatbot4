from django.conf import settings
from django.db import models
from django.utils import timezone

'''
models.py
- It works similar to the database that declares the class, requiremnents under the class
- It provides a structure of the data delivered along with the application
'''

class Chatting(models.Model):
    
    username = models.CharField(max_length=20, default='Alex Park')
    chatlog = models.CharField(max_length=10000, blank=True)

    def __str__(self):
        return str(self.username)