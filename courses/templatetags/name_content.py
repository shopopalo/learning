from django import template

register = template.Library()

@register.filter
def name_of_model(obj):
	try:
		return obj._meta.model_name
	except AttributeError:
		return None