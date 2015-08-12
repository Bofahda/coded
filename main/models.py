from django.db import models

# Create your models here.

class Manufacturer(models.Model):
	name = models.CharField(max_length=30, unique=True)

	def __unicode__(self):
		return "%s" % self.name

class Cereal(models.Model):
	cereal_name = models.CharField(max_length=30)
	type = models.CharField(max_length=30, null=True)
	manufacturer = models.ForeignKey('main.Manufacturer', null=True)

	def __unicode__(self):
		return "%s" % self.cereal_name

class Nutrition(models.Model):
	calories = models.IntegerField(null=True)
	protein_g = models.IntegerField(null=True)
	fat = models.IntegerField(null=True)
	sodium = models.IntegerField(null=True)
	dietary_fiber = models.FloatField(null=True)
	carbs = models.FloatField(null=True)
	sugars = models.FloatField(null=True)
	display_shelf = models.CharField(max_length=30, null=True)
	potassium = models.IntegerField(null=True)
	vitamins_and_minerals = models.CharField(max_length=30, null=True)
	serving_size_weight = models.CharField(max_length=30, null=True)
	cups_per_serving = models.CharField(max_length=30, null=True)
	cereal = models.OneToOneField('main.Cereal')
	
	def __unicode__(self):
		return self.cereal.cereal_name

	def nutrition_list(self):
		value_list = []
		value_list.append("Protein:%s"%self.protein_g)
		value_list.append("Calories:%s"%self.calories)
		value_list.append("Fat:%s"%self.fat)
		value_list.append("Sodium:%s"%self.sodium)
		value_list.append("Dietary Fiber:%s"%self.dietary_fiber)
		value_list.append("Carbs:%s"%self.carbs)
		value_list.append("Sugars:%s"%self.sugars)
		value_list.append("Display Shelf:%s"%self.display_shelf)
		value_list.append("Potassium:%s"%self.potassium)
		value_list.append("Vitamins and Minerals:%s"%self.vitamins_and_minerals)
		value_list.append("Serving Size Weight:%s"%self.serving_size_weight)
		value_list.append("Cups/Serving:%s"%self.cups_per_serving)

		return value_list






