
function add_inscription() {
	console.log( `called add_inscription()` );
}

function toggleformervalue( value, formerValue, targetElementId ) {
	const targetElement = document.getElementById( targetElementId );
	if ( targetElement ) {
		if ( value == formerValue ) {
			targetElement.classList.remove( 'value-has-changed' );
		} else {
			targetElement.classList.add( 'value-has-changed' );
		}
	}
}

function confirminscriptionremove() {
	const result = confirm("Delete this inscription?");
	return result;
}

function selectall( element ) {
	try {
		element.select()
	} catch (err) {
		console.log( `failed to select all in input ${element}` )
	}
}

function incrementimagekey( inputElementId, previewContainerElementId ) {
	adjustimagekey( inputElementId, previewContainerElementId, +1 );
}

function decrementimagekey( inputElementId, previewContainerElementId ) {
	adjustimagekey( inputElementId, previewContainerElementId, -1 );
}

function adjustimagekey( inputElementId, previewContainerElementId, delta ) {
	const inputElement = document.getElementById( inputElementId );
	const previewContainerElement = document.getElementById( previewContainerElementId );
	if ( inputElement && previewContainerElement ) {
		const previewElements = previewContainerElement.children;
		var index = 0;
		for ( var i = 0 ; i < previewElements.length ; ++i ) {
			const previewElement = previewElements[i];
			if ( previewElement.classList.contains( 'active' ) ) {
				index = i ;
				break;
			}
		}
		let newIndex = index + delta ;
		if ( newIndex >= previewElements.length ) {
			newIndex = 0 ;
		}
		if ( newIndex < 0 ) {
			newIndex =  previewElements.length - 1 ;
		}
		previewElements[index].classList.remove( 'active' )
		previewElements[newIndex].classList.add( 'active' )
		for ( var className of previewElements[newIndex].classList ) {
			if ( className.startsWith( 'badge-image-key-' ) ) {
				const newValue = className.substring( 'badge-image-key-'.length ) ;
				inputElement.value = newValue ;
			}
		}
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