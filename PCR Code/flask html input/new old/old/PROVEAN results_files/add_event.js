/**
 * This function adds an event to a certain event. This is done so the onload calls can be 
 * unobtrusive and dynamic. This function comes from 
 * http://onlinetools.org/articles/unobtrusivejavascript/chapter4.html.
 *  @param obj : the object to load the event to
 *  @param evType : the event indicating when to execute the function
 *  @param fn : the function to execute
 *  @return : true or false depending on the success of the execution
 */
function addEvent(obj, evType, fn) { 
  if(obj.addEventListener) { 
    obj.addEventListener(evType, fn, false); 
    return true; 
  } // end if(obj.addEventListener)
  else if(obj.attachEvent) { 
    var r = obj.attachEvent("on" + evType, fn); 
    return r; 
  } // end else if (obj.attachEvent) 
  else { 
    return false; 
  } // end else
} // end function addEvent(obj, evType, fn)vim 