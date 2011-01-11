
/*
Handle click events on the widget. This lets us tell about the event itself.
*/
this.addEventListener('click', function(e) {

  // This is a left click, with no shift key
  if(e.button == 0 && e.shiftKey == false) {
    postMessage('left-click');
  }

  // This is a right click, or a left click with shift key (treat like right)
  if(e.button == 2 || (e.button == 0 && e.shiftKey == true)) {
    postMessage('right-click');
  }
  e.preventDefault();
}, true);

