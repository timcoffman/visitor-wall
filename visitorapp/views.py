from django.http import QueryDict
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse
from django.db.models import Q

from datetime import datetime, timedelta
import colorsys
import random

from .models import Wall, Visitor, Inscription
from .layouts import HEXAGONAL_LAYOUTS
from .badge_images import BADGE_KEYS, BADGE_IMAGES 

def about(request):
	context = {	}
	return render( request, "visitorapp/about.html", context )

def index(request):
	context = {
		'wall_list': Wall.objects.order_by('-created_date'),
	}
	return render( request, "visitorapp/index.html", context )


def show_wall(request, wall_id ):
	tutorialOverride = 'tutorial' in request.GET

	wall = get_object_or_404( Wall, pk=wall_id )
	visitor = current_visitor( request )
	datetime_cutoff = datetime.now() - timedelta(hours=1, minutes=0)
	query = (
		Q(moderation_status='ok') | # show because it's been reviewed and is ok
		(
			Q(visitor_id=visitor.id) & # show because this visitor wrote it ...
			~Q(moderation_status='removed') # ... and it hasn't been removed
		) |
		(
			Q(moderation_status='new') & # show because it hasn't been moderated ...
			Q(created_date__gte=datetime_cutoff)  # ... but it was just created recently
		)
	)
	inscriptions = wall.inscription_set.filter(query).order_by('-id');

	editInscription = int(request.GET['editInscription']) if 'editInscription' in request.GET else None

	layout_size, layout = next( ( (n,hl) for (n,hl) in enumerate(HEXAGONAL_LAYOUTS) if len(hl) > len(inscriptions) ), None )
	normalized_layout = [ { 'x': int(xy['x'] * 100 + 50), 'y': int(xy['y'] * 100 + 50) } for xy in layout ]

	badgeList = [
		make_badge(
			i,
			visitor,
			normalized_layout[n],
			0.5 * n / len(inscriptions),
			editInscription == i.id
			)
		for n, i
		in enumerate(inscriptions)
		]
	editBadge = next( (b for b in badgeList if b['id'] == editInscription), None )

	myBadgeList = [ b for b in badgeList if b['is_mine'] ]
	tutorial = tutorialOverride or len(myBadgeList) == 0

	context = {
		'wall': wall,
		'edit_inscription': editInscription,
		'badge_list': badgeList,
		'badge_layout_size': layout_size,
		'edit_badge': editBadge,
		'tutorial': tutorial,
	}
	return render( request, "visitorapp/wall.html", context )

def current_visitor( request ):
	if request.session.session_key is None:
		request.session.save()
	visitor, visitor_created = Visitor.objects.get_or_create( cookie=request.session.session_key, defaults={} )
	return visitor

def make_badge( inscription, currentVisitor, position, animationDelaySeconds, isSelected ):
	signature = inscription.signature
	if signature is None or len(signature) == 0:
		textWithSignature = inscription.text
	else:
		textWithSignature = inscription.text + ' -' + signature

	bg = bg_from_int( inscription.id )
	skew = skew_from_int( inscription.id )
	editorLocation = 'upper' if position['y'] > 50 else 'lower'

	imageKey = inscription.image_override
	if imageKey is None or len(imageKey) == 0:
		checkImageKey = image_key_from_int( inscription.id )
		if checkImageKey in BADGE_KEYS:
			imageKey = checkImageKey
	staticImage = BADGE_IMAGES[ imageKey ]

	if isSelected:
		badgeImages = [ { 'key': k, 'src': BADGE_IMAGES[k] } for k in BADGE_KEYS ]
		random_from_int( inscription.id ).shuffle( badgeImages )
	else:
		badgeImages = None

	badge = {
		'id': inscription.id,
		'text': inscription.text,
		'signature': inscription.signature,
		'text_with_signature': textWithSignature,
		'image_key': imageKey,
		'badge_images': badgeImages,
		'static_image': staticImage,
		'is_mine': currentVisitor.id == inscription.visitor_id,
		'is_selected': isSelected,
		'position': position,
		'skew': skew,
		'anim_delay': f'{animationDelaySeconds:0.2f}s',
		'bg': bg,
		'editor_location': editorLocation,
		}
	return badge

def random_from_int( n ):
	return random.Random(n)

POS_M = 27644437
POS_D = 1932.0

def position_from_int( n ):
	q = ( n * POS_M ) % (POS_D*POS_D)
	x = (q // POS_D) / POS_D
	y = (q % POS_D) / POS_D
	return { 'x': int(x * 100), 'y': int(y * 100) }

def skew_from_int( n ):
	q = ( n * POS_M ) % (POS_D)
	k = q / POS_D * 10.0 - 5.0
	return k

def bg_from_int( n ):
	q = ( n * POS_M ) % (POS_D)
	h = q / POS_D * 1.00
	rgb = colorsys.hsv_to_rgb( h, 0.07, 1.0 )
	return f'#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}'

def image_key_from_int( n ):
	i = n % len(BADGE_KEYS)
	k = BADGE_KEYS[ i ]
	return k

INITIAL_TEXT = 'inscribe your message here'

def add_inscription(request, wall_id):
	wall = get_object_or_404( Wall, pk=wall_id )
	visitor = current_visitor( request )
	inscription = Inscription.objects.create(
		wall=wall,
		visitor=visitor,
		text=INITIAL_TEXT,
		moderation_status='new',
		created_date=datetime.now()
		)
	q = QueryDict(mutable=True)
	q['editInscription'] = inscription.id
	return redirect( reverse( 'show_wall', args=(wall.id,), query=q ) )

def update_inscription(request, wall_id, inscription_id):
	wall = get_object_or_404( Wall, pk=wall_id )
	visitor = current_visitor( request )
	inscription = get_object_or_404( Inscription, pk=inscription_id )
	if ( visitor.id != inscription.visitor_id ):
		return HttpResponse( f'not authorized to change this inscription', status=401)
	if 'destroy' in request.POST:
		print( f'POST.destroy = {request.POST["destroy"]}' )
		inscription.moderation_status = 'removed'
	if 'commit' in request.POST:
		print( f'POST.commit = {request.POST["commit"]}' )
		inscription.text = request.POST['text']
		if 'signature' in request.POST:
			inscription.signature = request.POST['signature']
		if 'image-key' in request.POST:
			imageKey = request.POST['image-key']
			if imageKey in BADGE_KEYS:
				inscription.image_override = imageKey 
	inscription.save()
	return redirect( reverse( 'show_wall', args=(wall.id,) ) )
