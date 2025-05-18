
function add_inscription() {
	console.log( `called add_inscription()` );
}

function toggleformervalue( value, formerValue, targetElementId ) {
	const targetElement = document.getElementById( targetElementId );
	if ( targetElement ) {
		const shouldShow = value != formerValue ;
		targetElement.style['display'] = shouldShow ? '' : 'none' ;
	}
}

function selectall( element ) {
	try {
		element.select()
	} catch (err) {
		console.log( `failed to select all in input ${element}` )
	}
}

addEventListener( 'load', () => {
	try {
		inscription_autofocus = document.getElementById('inscription_autofocus');
		if ( inscription_autofocus ) {
			inscription_autofocus.focus();
		}
	} catch (err) {
		console.log( `failed to attach inscription autofocus at load time` )
	}
});