from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import PincodeData, UserInputModel
import scipy.io as sio
import numpy as np
import lr
import adval
import json

def validate_input(request):
	if not request.POST.get('email', False):
		return False
	else:
		try:
			validate_email(request.POST['email'])
		except ValidationError as e:
			return False
	if not request.POST.get('amount', False):
		return False
	else:
		try:
			x = int(request.POST['amount'])
		except:
			return False
	if not request.POST.get('address1', False):
		return False
	if not request.POST.get('address2', False):
		return False
	if not request.POST.get('city', False):
		return False
	if not request.POST.get('pincode', False):
		return False
	else:
		try:
			x = int(request.POST['pincode'])
		except:
			return False
	return True

def predict_x(request):
	b = sio.loadmat('trained_val.mat')
	try:
		pd = PincodeData.objects.get(pincode=int(request.POST.get('pincode')))
	except:
		pd = PincodeData.objects.create(pincode=int(request.POST.get('pincode')))
		pd.save()
	try:
		ud = UserInputModel.objects.get(user_email=request.POST.get('email'))
	except:
		ud = UserInputModel.objects.create(user_email=request.POST.get('email'))
		ud.save()
	pd = PincodeData.objects.get(pincode=int(request.POST.get('pincode')))
	ud = UserInputModel.objects.get(user_email=request.POST.get('email'))
	x = np.array([pd.pincode_success_rate, ud.user_theft, 0, ud.user_success_rate, request.POST.get('amount'), ud.user_succesful_transactions], dtype=float)
	theta = b['theta']
	b.pop('theta', None)
	y = lr.predict(theta, x, b)
	if y:
		return render_to_response('result.html', {'res' : 'You can order with both options'}, context_instance=RequestContext(request))
	else:
		x[2] = 1
		y = lr.predict(theta, x, b)
		if y:
			return render_to_response('result.html', {'res': 'Cash on delivery is not available'}, context_instance=RequestContext(request))
		else:
			return render_to_response('result.html', {'res': 'We do not deliver to this address'}, context_instance=RequestContext(request))

def delivery_report(request):
	if request.method == 'GET':
		return render_to_response('report.html', context_instance = RequestContext(request))
	elif request.method == 'POST':
		email = request.POST.get('email')
		pincode = int(request.POST.get('pincode'))
		success = int(request.POST.get('delivery_successful_or_not'))
		ud = UserInputModel.objects.get_or_create(user_email = email)[0]
		pd = PincodeData.objects.get_or_create(pincode=pincode)[0]
		
		ud.user_succesful_transactions += success
		ud.user_total_transactions += 1
		ud.user_success_rate = ud.user_succesful_transactions * 1.0 / ud.user_total_transactions
		ud.save()
	
		pd.pincode_successful_transactions += success
		pd.pincode_total_trasactions += 1
		pd.pincode_success_rate = pd.pincode_successful_transactions * 1.0 / pd.pincode_total_trasactions
		pd.save()

		return render_to_response('report.html', {'res' : 'success'}, context_instance = RequestContext(request))


@csrf_protect
def index(request) :
	if request.method == 'GET':
		return train(request)
		# return render_to_response('index.html', context_instance = RequestContext(request))
	elif request.method == 'POST':
		# print request.POST.get('pincode')
		# print request.POST.get('city')
		# print validate_input(request)
		# print adval.validate_pincode(request.POST.get('pincode'), request.POST.get('city'))
		# print adval.check_address(request.POST.get('pincode'), str(request.POST.get('address1')), request.POST.get('city'), 'India')
		if validate_input(request) and adval.validate_pincode(request.POST.get('pincode'), request.POST.get('city')) and adval.check_address(request.POST.get('pincode'), str(request.POST.get('address1')), request.POST.get('city'), 'India'):
			return predict_x(request)
		else:
			return render_to_response('index.html', {'msg' : 'Please provide valid input'}, context_instance = RequestContext(request))

def train(request):
	theta, mean, minv, maxv = lr.train()
	a = {'theta':theta, 'mean':mean, 'minv':minv, 'maxv':maxv}
	sio.savemat('trained_val.mat', a)
	return render_to_response('index.html', {'msg' : 'successfully trained model'}, context_instance = RequestContext(request))

