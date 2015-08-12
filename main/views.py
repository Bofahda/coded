from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from main.models import Manufacturer,Cereal
from main.forms import CerealSearch, CreateCereal, UserLogin

from django.template import RequestContext

def first_view(request):

	manufacturers = Manufacturer.objects.all()


	# manufacturer_list = ""
	cereal_string = """
	<style>
	.boxed:nth-child(even) {
		border: 1px solid green;
		background-color: orange;
		}
	.boxed:nth-child(odd) {
		border: 1px solid green;
		background-color: green;
		}
	.headings {border: 1px solid #CCC;
				background-color: rgb(208,200,200)}
	</style>
	"""

	for manufacturer in manufacturers:
		
		cereal_string += "<h4>%s</h4>" % manufacturer

		for cereal in manufacturer.cereal_set.all():
			cereal_string += "<div class=headings><b>Manufacturer:</b> %s,</br><b>Cereal:</b> %s,</div><div class='boxed'></br><b><u>Nutrition Facts:</b></u></br> Calories: %s,</br> Protein (g): %s,</br> Fat: %s,</br> Sodium: %s,</br> Dietary Fiber: %s,</br> Carbs: %s,</br> Sugars: %s,</br> Display Shelf: %s,</br> Potassium: %s,</br> Vitamins and Minerals: %s,</br> Serving Size Weight: %s,</br> Cups Per Serving: %s</br></br></div>" % (manufacturer.name, 
					cereal.cereal_name, 
					cereal.nutrition.calories,
					cereal.nutrition.protein_g,
					cereal.nutrition.fat,
					cereal.nutrition.sodium,
					cereal.nutrition.dietary_fiber,
					cereal.nutrition.carbs,
					cereal.nutrition.sugars,
					cereal.nutrition.display_shelf,
					cereal.nutrition.potassium,
					cereal.nutrition.vitamins_and_minerals,
					cereal.nutrition.serving_size_weight,
					cereal.nutrition.cups_per_serving


											)

	return HttpResponse (cereal_string)

def cereal_list_template(request):

	manufacturers = Manufacturer.objects.all()

	context = {}

	context['manufacturers'] = manufacturers

	return render(request, 'cereal_list.html', context)

def logout_view(request):

	logout(request)

	return HttpResponseRedirect('/login_view/')

def cereal_list_template2(request):

	manufacturers = Manufacturer.objects.all()

	context = {}

	manufacturer_cereal = {}

	for manufacturer in manufacturers:
		cereals = manufacturer.cereal_set.filter(name__contains="A")

		manufacturer.name = { manufacturer.name : cereals }

		manufacturer_cereal.update(manufacturer.name)

	context['manufacturer_cereal'] = manufacturer_cereal


	return render(request, 'cereal_list2.html', context)

def login_view(request):
	context = {}

	context['form'] = UserLogin()

	username = request.POST.get('username', None)
	password = request.POST.get('password', None)

	auth_user = authenticate(username=username, password=password)

	if auth_user is not None:
		if auth_user.is_active:
			login(request, auth_user)
			context['valid'] = "Login Successful"

			return HttpResponseRedirect('/home')
		else:
			context['valid'] = "Go Away"
	else:
		context['valid'] = "Please enter a User Name"

	return render_to_response('login.html', context, context_instance=RequestContext(request))


def cereal_detail(request,pk):
	
	context ={}
	
	manus = Manufacturer.objects.all()
	context['manus'] = manus

	cereal = Cereal.objects.get(pk=pk)
	context['cereal'] = cereal

	return render_to_response('cereal_detail.html', context, context_instance=RequestContext(request))	



def cereal_search(request, cereal):

	cereals = Cereal.objects.filter(cereal_name__istartswith=cereal_name)

	cereal_string = ""

	for cereal in cereals:
		cereal_string += "<b>Cereal:</b>%s, <b>Manufacturer:</b> %s </br>" % (cereal.cereal_name, cereal.manufacturer)

	return HttpResponse(cereal_string)

def get_cereal_search(request):

	cereal_name = request.GET.get('cereal')
	manufacturer = request.GET.get('manufacturer')

	cereal_string = """
	<form action>
	<style>
	.boxed:nth-child(even) {
		border: 1px solid green;
		background-color: orange;
		}
	.boxed:nth-child(odd) {
		border: 1px solid green;
		background-color: rgb(208,200,200);
		}
			</style>
	Cereal:
	
	<input type="text" name="cereal"></br>

	Manufacturer:
	<input type="text" name="manufacturer">

	</br>
	<input type="submit" value="Submit">
	</form>
	"""
	manufacturer_string = ""

	if cereal_name:
		cereals = Cereal.objects.filter(cereal_name__istartswith=cereal_name)
		for cereal in cereals:
			cereal_string += "<div class='boxed'>%s</br></div>" % cereal.cereal_name

	
	if manufacturer:
		manufacturers = Manufacturer.objects.filter(name__contains=manufacturer)
		for manufacturer in manufacturers:
			manufacturer_string += "<div class='boxed2'>%s</br></div>" % manufacturer.name
	
	cereal_string += manufacturer_string

	return HttpResponse(cereal_string)

def home(request):

	# context = {}

	# manus = Manufacturer.objects.all()

	# context['manus'] = manus

	return render_to_response('home.html', {}, context_instance=RequestContext(request))

def cereal_create(request):

	context = {}

	form = CreateCereal()
	context['form'] = form


	if request.method == 'POST':
		form = CreateCereal(request.POST)

		if form.is_valid():
				form.save()

				context['valid'] = "Cereal Saved"

	elif request.method == 'GET':
		context['valid'] = form.errors

	return render_to_response('cereal_create.html', context, context_instance=RequestContext(request))

def form_view(request):

	context = {}

	get = request.GET
	post = request.POST

	context['get'] = get
	context['post'] = post

	if request.method == "POST":
		cereal = request.POST.get('cereal', None)

		cereals = Cereal.objects.filter(cereal_name__startswith=cereal)

		context['cereals'] = cereals

	elif request.method == "GET":
		context['method'] = 'The method was GET'

	return render_to_response('form_view.html', context, context_instance=RequestContext(request))

def form_view2(request):

	context = {}

	get = request.GET
	post = request.POST

	context['get'] = get
	context['post'] = post

	# context['form'] = cereal_search
	form = CerealSearch()

	context['form'] = form


	if request.method == "POST":
		form = CerealSearch(request.POST)

		if form.is_valid():
			# cereal = request.POST.get('name', None)
			cereal = form.cleaned_data['name']

			cereals = Cereal.objects.filter(cereal_name__startswith=cereal)

			context['cereals'] = cereals
			context['valid'] = "The Form Was Valid"
		else: 
			context['valid'] = form.errors

	elif request.method == "GET":
		context['method'] = 'The method was GET'
		
	return render_to_response('form_view2.html', context, context_instance=RequestContext(request))




def nutrition_search(request, cereal, manufacturer):

	manufacturers = Manufacturer.objects.all()

	print manufacturers

	nutrition_string = ""

	for manufacturer in manufacturers:
		print manufacturer
		print manufacturer.cereal_set.all()
		cereals = manufacturer.cereal_set.filter(cereal_name__istartswith=cereal)
		print cereals
		for cereal in cereals:
			nutrition_string += "Manufacturer:%s,</br> Cereal: %s,</br> Calories: %s,</br> Protein (g): %s,</br> Fat: %s,</br> Sodium: %s,</br> Dietary Fiber: %s,</br> Carbs: %s,</br> Sugars: %s,</br> Display Shelf: %s,</br> Potassium: %s,</br> Vitamins and Minerals: %s,</br> Serving Size Weight: %s,</br> Cups Per Serving: %s</br></br>" % (manufacturer.name, 
												cereal.cereal_name, 
												cereal.nutrition.calories,
												cereal.nutrition.protein_g,
												cereal.nutrition.fat,
												cereal.nutrition.sodium,
												cereal.nutrition.dietary_fiber,
												cereal.nutrition.carbs,
												cereal.nutrition.sugars,
												cereal.nutrition.display_shelf,
												cereal.nutrition.potassium,
												cereal.nutrition.vitamins_and_minerals,
												cereal.nutrition.serving_size_weight,
												cereal.nutrition.cups_per_serving


											)

	return HttpResponse(nutrition_string)

from django.contrib.auth.models import User
from main.forms import UserSignUp
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

def signup(request):

	context = {}

	form = UserSignUp()
	context['form'] = form

	if request.method == 'POST':
		form = UserSignUp(request.POST)
		if form.is_valid():

			name = form.cleaned_data['name']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']

			try:
				new_user = User.objects.create_user(name, email, password)
				context['valid'] = "Thank You For Signing Up!"

				auth_user = authenticate(username=name, password=password)
				login(request, auth_user)
				HttpResponseRedirect('/cereal_list_template/')

			except IntegrityError, e:
				context['valid'] = "A User With That Name Already Exists"

		else:
			context['valid'] = form.errors


	if request.method == 'GET':
		context['valid'] = "Please Sign Up!"


	return render_to_response('signup.html', context, context_instance=RequestContext(request))

