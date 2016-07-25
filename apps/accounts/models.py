from __future__ import unicode_literals
from django.db import models

class User(models.Model):
	username = models.CharField(max_length=100)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	updated_at = models.DateTimeField(auto_now_add=True, blank=True)
	def __str__(self):
		return self.username
	class Meta:
		db_table = 'users'