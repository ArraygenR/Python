/**
 * This function assigns the target="_blank" attribute to all external links. That is not 
 * added directly to the links because the attribute is deprecated. Also, this function is 
 * assigned to the onload function so that the JavaScript is unobtrusive.
 * @return void
 */ 
function set_external_navigation() { 
  if(!document.getElementsByTagName) { 
    return;
  } // end if(!document.getElementsByTagName)
  
  var links = document.getElementsByTagName('a');
  
  for(var i = 0, link; link = links[i]; i++) { 
    if(link.getAttribute('rel') == 'external') { 
      link.setAttribute('target', '_blank');
    } // end if(link.getAttribute('rel') == 'external')
  } // end for(var i = 0, link; link = links[i]; i++)
} // end function set_external_navigation()

addEvent(window, 'load', set_external_navigation);