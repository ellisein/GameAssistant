from django import template


register = template.Library()

@register.filter(name='dict_value')
def dict_value(dict_data, key):
	if key in dict_data:
		return dict_data[key]

@register.filter(name='join')
def join_with_commas(obj_list):
	if not obj_list:
		return ''
	return ', '.join(obj_list)
