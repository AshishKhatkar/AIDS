from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import adval.py

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

@csrf_protect
def index(request) :
	if request.method == 'GET':
		return render_to_response('index.html', context_instance = RequestContext(request))
	elif request.method == 'POST':
		if validate_input(request):
			return HttpResponse('Congrats, fuck you')
		else:
			return render_to_response('index.html', {'msg' : 'Please provide valid input'}, context_instance = RequestContext(request))

