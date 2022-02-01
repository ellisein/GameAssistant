from django.urls import path

from . import views


urlpatterns = [
	path('', views.default),
	path('wow/character', views.wow_character),
	path('wow/mythic-keystone', views.wow_mythic_keystone),
	path('anno/calculator', views.anno_calculator),
	path('minecraft/user', views.minecraft_user),
]
