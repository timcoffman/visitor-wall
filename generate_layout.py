
import random;
import math;

R = random.Random(7789)

PATTERNS = []

LAYOUT = [ (0,0) ]
PATTERNS.append( LAYOUT[:] )

SQRT3_2 = math.sqrt(3.0)/2.0
RING = 1
while RING < 7:
	for i in range(RING):
		LAYOUT.append( ( -i, +RING ) )
		LAYOUT.append( ( +i, -RING ) )
	for i in range(RING):
		LAYOUT.append( ( -RING, +RING-i ) )
		LAYOUT.append( ( +RING, -RING+i ) )
	for i in range(RING):
		LAYOUT.append( ( -RING+i, -i ) )
		LAYOUT.append( ( +RING-i, +i ) )
	layout = [ ( xy[0] + xy[1]/2, xy[1] * SQRT3_2 ) for xy in LAYOUT ]
	x_max = max( [ xy[0] for xy in layout ])
	y_max = max( [ xy[1] for xy in layout ])
	normalized_layout = [ (xy[0]*0.5/x_max, xy[1]*0.5/y_max) for xy in layout ] 
	R.shuffle( normalized_layout )
	PATTERNS.append( normalized_layout )
	RING = RING + 1

for i in range(len(PATTERNS)):
	print( f'HEXAGONAL_LAYOUT_{i} = [' )
	for XY in PATTERNS[i]:
		print( f'\t{{ "x": {XY[0]:.2f}, "y": {XY[1]:.2f} }},' )
	print( f']' )

print( '' )

print( f'HEXAGONAL_LAYOUTS = [' )
for i in range(len(PATTERNS)):
	print( f'\tHEXAGONAL_LAYOUT_{i},' )
print( f']' )
		
