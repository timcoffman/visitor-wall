from django.urls import path

from . import views
from . import views_svg
from . import views_svg2

urlpatterns = [
	path( '', views.index, name="index" ),
	path( 'wall/<int:wall_id>/', views.show_wall, name="show_wall" ),
	path( 'wall/<int:wall_id>/inscribe/', views.add_inscription, name="add_inscription" ),
	path( 'banner/draw', views_svg.draw_banner, name="draw_banner" ),
	path( 'banner/draw2', views_svg2.draw_banner, name="draw_banner2" ),
]

