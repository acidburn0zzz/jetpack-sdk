/*
Locate anchors for annotations and prepare to display the annotations.

For each annotation, if its URL matches this page,
- get the ancestor whose ID matches the ID in the anchor
- look for a <p> element whose content contains the anchor text

That's considered a match: then we:
- highlight the anchor element
- add an 'annotated' class to tell the selector to skip this element
- bind 'mouseover' and 'mouseout' events to the element, to send 'show'
and 'hide' messages back to the add-on.
*/

self.on('message', function onMessage(annotations) {
  annotations.forEach(
    function(annotation) {
      if(annotation.url == document.location.toString()) {
        displayAnnotation(annotation);
      }
  })
})

function displayAnnotation(annotation) {
  annotationAnchorAncestor = $('#' + annotation.ancestorId);
  annotationAnchor = $(annotationAnchorAncestor).find(
                     'p:contains(' + annotation.anchorText + ')').last();
  $(annotationAnchor).css('border', 'solid 3px yellow');
  $(annotationAnchor).addClass('annotated');
  $(annotationAnchor).bind('mouseover', function() {
    postMessage(['show', annotation.annotationText]);
  });
  $(annotationAnchor).bind('mouseout', function() {
    postMessage(['hide']);
  });
}
