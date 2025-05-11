from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Wall, Visitor, Inscription

def index(request):
	context = {
		'wall_list': Wall.objects.order_by('-created_date'), 
	}
	return render( request, "visitorapp/index.html", context )

def show_wall(request, wall_id ):
	visitor = current_visitor( request )
	inscriptions = Inscription.objects.order_by('-id');
	context = {
		'wall': get_object_or_404( Wall, pk=wall_id ),
		'badge_list': [ make_badge(i,visitor) for i in inscriptions ]
	}
	return render( request, "visitorapp/wall.html", context )

def current_visitor( request ):
	if request.session.session_key is None:
		request.session.save()
	visitor, visitor_created = Visitor.objects.get_or_create( cookie=request.session.session_key, defaults={} )
	return visitor

def make_badge( inscription, currentVisitor ):
	badge = {
		'id': inscription.id,
		'text': inscription.text,
		'isMine': currentVisitor.id == inscription.visitor_id,
		'position': position_from_int( inscription.id ),
		}
	return badge

def position_from_int( n ):
	q = ( n * 7919 ) % (83*83)
	x = (q // 83) / 83.0
	y = (q % 83) / 83.0
	return { 'x': int(x * 100), 'y': int(y * 100) } 

def add_inscription(request, wall_id):
	wall = get_object_or_404( Wall, pk=wall_id )
	visitor = current_visitor( request )
	inscription = Inscription.objects.create( wall=wall, visitor=visitor, text=request.POST['inscription_text'] )
	return redirect( reverse( 'show_wall', args=(wall.id,) ) )
