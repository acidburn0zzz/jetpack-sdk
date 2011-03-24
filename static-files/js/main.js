function run(jQuery) {
  const IDLE_PING_DELAY = 5000;

  function highlightCode() {
    $("code").parent("pre").addClass("brush: js");
    //remove the inner <code> tags
    $('pre>code').each(function() {
      var inner = $(this).contents();
      $(this).replaceWith(inner);
    })
    SyntaxHighlighter.highlight();
  }

  function highlightCurrentPage() {
    var base_url = $("base").attr("href");
    $(".current-page").removeClass('current-page');
    $(".current-section").removeClass('current-section');

    if (base_url == '/')
      currentPage = window.location.pathname;
    else
      currentPage = window.location.toString();

    currentPage = currentPage.slice(base_url.length);
    $('a[href="' + currentPage + '"]').parent().addClass('current-page');

    currentSideBarSection = null;
    if ( $('.current-page').hasClass('sidebar-section-header') ) {
      currentSideBarSection = $('.current-page').next();
    }
    else {
      currentSideBarSection =
        $('.current-page').closest('.sidebar-section-contents');
    }
    if ($(currentSideBarSection).length == 0)
      currentSideBarSection = $('#default-section-contents');

    $('.sidebar-section-contents').hide();
    $(currentSideBarSection).parent().addClass('current-section');
    $(currentSideBarSection).show();
  }

  function generateToC() {
    var select = '.api-reference  h2,.api_reference h3, .api_reference h4, ' +
                 '.api_reference h5, .api_reference h6';
    $(select).each(function(i) {
      var link = document.location + "#title" + i;
      var current = $(this);
      var dataTypeStart = current.html().indexOf(" : ");
      var tocName = current.html();
      if (dataTypeStart != -1)
        tocName = tocName.slice(0, dataTypeStart);
      current.attr("id", "title" + i);
      $("#toc").append("<a id='link" + i + "' href='" +
        link + "' title='" + current.attr("tagName") + "'>" + 
        tocName + "</a>");
      });
  }

  var serverNeedsKeepalive = true;

  function sendIdlePing() {
    jQuery.ajax({url:"/api/idle",
               error: function(req) {
                 if (req.status == 501 || req.status == 404) {
                   // The server either isn't implementing idle, or
                   // we're being served from static files; just bail
                   // and stop pinging this API endpoint.
                   serverNeedsKeepalive = false;
                 }
               }});
    scheduleNextIdlePing();
  }

  function scheduleNextIdlePing() {
    if (serverNeedsKeepalive)
      window.setTimeout(sendIdlePing, IDLE_PING_DELAY);
  }

  if (window.location.protocol != "file:")
    scheduleNextIdlePing();
  highlightCurrentPage();
  highlightCode();
  generateToC();
}

$(window).ready(function() {
  run(jQuery);
});
