from django.contrib import admin

from main.models import Manufacturer, Cereal, Nutrition

# Register your models here.

class ManufacturerAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	


admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Cereal)
admin.site.register(Nutrition)