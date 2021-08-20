from django.urls import path
from . import views

app_name = "leagues"
urlpatterns = [
	path('', views.lvl2, name="index"),
	path('all-data', views.index, name="all-data"),
	path('lvl1', views.lvl1, name="lvl1"),
	path('lvl2', views.lvl2, name="lvl2"),
	path('initialize', views.make_data, name="make_data"),
]
