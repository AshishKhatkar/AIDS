from __future__ import unicode_literals

from django.db import models

class UserInputModel(models.Model):
	user_email = models.CharField(primary_key=True, max_length=50)
	user_succesful_transactions = models.IntegerField(default=0)
	user_total_transactions = models.IntegerField(default=0)
	user_success_rate = models.FloatField(default=1.0)
	user_theft = models.BooleanField(default=False)

	def __str__(self):
		res = '{"Email" : "' + str(self.user_email) + '", "Successful Transactions" : ' + str(self.user_succesful_transactions)
		res += ', "Total Transactions" : ' + str(self.user_total_transactions) + ', "Success Rate" : ' + str(self.user_success_rate)
		res += ', "Thief" : ' + str(self.user_theft)
		return res

class PincodeData(models.Model):
	pincode = models.CharField(primary_key=True, max_length=6)
	pincode_success_rate = models.FloatField(default=1.0)
	pincode_successful_transactions = models.IntegerField(default=0)
	pincode_total_trasactions = models.IntegerField(default=0)

	def __str__(self):
		res = '{"Pincode" : ' + str(self.pincode) + ', "Successful Transactions" : ' + str(self.pincode_successful_transactions)
		res += ', "Total Transactions" : ' + str(self.pincode_total_trasactions) + ', "Success Rate" : ' + str(self.pincode_success_rate)
		return res