import ast
from django.db import models
from django.contrib.auth.forms import User

class ListField(models.TextField):
	description = "Stores a python list"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def from_db_value(self, value, expression, connection):
		if value is None:
			return value
		if isinstance(value, str):
			return value.split(',')

	def to_python(self, value):
		if not value:
			value = []
		if isinstance(value, list):
			return value
		if isinstance(value, str):
			return ast.literal_eval(value)

	def get_prep_value(self, value):
		if value is None:
			return value
		if value is not None and isinstance(value, str):
			return value
		if isinstance(value, list):
			return ','.join(value)

	def value_to_string(self, obj):
		value = self.value_from_object(obj)
		return self.get_prep_value(value)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    balance = models.IntegerField()
    transactions = models.IntegerField(null=False, blank=True, default=0)
    balanceSpent = models.IntegerField(null=False, blank=True, default=0)
    history = ListField(null=False, blank=True)

    def __str__(self):
        return self.user.username
