from django.urls import path

from . import views
from . import views_svg

urlpatterns = [
	path( '', views.index, name="index" ),
	path( 'about', views.about, name="about" ),
	path( 'wall/<int:wall_id>/', views.show_wall, name="show_wall" ),
	path( 'wall/<int:wall_id>/inscribe/', views.add_inscription, name="add_inscription" ),
	path( 'wall/<int:wall_id>/inscription/<int:inscription_id>', views.update_inscription, name="update_inscription" ),
	path( 'ring/draw', views_svg.draw_ring, name="draw_ring" ),
	path( 'banner/draw', views_svg.draw_banner, name="draw_banner" ),
]

