#!/usr/bin/env python
import csv
import os
import sys


sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from main.models import Manufacturer, Cereal, Nutrition

Manufacturer.objects.all().delete()
Cereal.objects.all().delete()
Nutrition.objects.all().delete()

csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"cereal.csv")
csv_file = open(csv_file_path, 'r')

print csv_file
reader = csv.DictReader(csv_file)

print reader
for row in reader:
	print row['Cereal Name'].replace('_',' ')
	#print row['Manufacturer']

	manu_obj, created = Manufacturer.objects.get_or_create(name=row['Manufacturer'])

	cereal_obj, created = Cereal.objects.get_or_create(cereal_name=row['Cereal Name'].replace('_',' '))
	cereal_obj.type = row['Type']
	cereal_obj.manufacturer = manu_obj

	cereal_obj.save()

	nutri_obj, created = Nutrition.objects.get_or_create(cereal=cereal_obj)
	nutri_obj.calories = row['Calories']
	nutri_obj.protein_g = row['Protein (g)']
	nutri_obj.fat = row['Fat']
	nutri_obj.sodium = row['Sodium']
	nutri_obj.dietary_fiber = row['Dietary Fiber']
	nutri_obj.carbs = row['Carbs']
	nutri_obj.sugars = row['Sugars']
	nutri_obj.display_shelf = row['Display Shelf']
	nutri_obj.potassium = row['Potassium']
	nutri_obj.vitamins_and_minerals = row['Vitamins and Minerals']
	nutri_obj.serving_size_weight = row['Serving Size Weight']
	nutri_obj.cups_per_serving = row['Cups per Serving']

	try:
		nutri_obj.save()
	except Exception, a:
		print a
		print row['Cereal Name']


	# print row['Type']
	# print row['Calories']
	# print row['Protein (g)']
	# print row['Fat']
	# print row['Sodium']
	# print row['Dietary Fiber']
	# print row['Carbs']
	# print row['Sugars']
	# print row['Display Shelf']
	# print row['Potassium']
	# print row['Vitamins and Minerals']
	# print row['Serving Size Weight']
	# print row['Cups per Serving']
