
var document = window.document;
var currentPage = "";
var shouldFadeAndScroll = true;

const DEFAULT_PAGE = "/guide/welcome";
const DEFAULT_SIDEBAR_SECTION = "#guide/addon-development/about";
const IDLE_PING_DELAY = 500;
const DOCUMENT_TITLE_ROOT = "Add-on SDK Documentation";

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
  $(".current-page").removeClass('current-page');
  $(".current-section").removeClass('current-section');
  currentPage = window.location.pathname;
  if (currentPage.length <= 1) {
    currentSideBarSection = $('#default-section-contents');
  }
  else {
    $('a[href="' + currentPage + '"]').parent().addClass('current-page');
    currentSideBarSection = null;
    if ( $('.current-page').hasClass('sidebar-section-header') ) {
      currentSideBarSection = $('.current-page').next();
    }
    else {
      currentSideBarSection = $('.current-page').closest('.sidebar-section-contents');
    }
  }
  $('.sidebar-section-contents').hide();
  $(currentSideBarSection).parent().addClass('current-section');
  $(currentSideBarSection).show();
}

var isPingWorking = true;

function sendIdlePing() {
  jQuery.ajax({url:"/api/idle",
               // This success function won't actually get called
               // for a really long time because it's a long poll.
               success: scheduleNextIdlePing,
               error: function(req) {
                 if (req.status == 501 || req.status == 404)
                   // The server either isn't implementing idle, or
                   // we're being served from static files; just bail
                   // and stop pinging this API endpoint.
                   return;
                 if (id) {
                   window.clearTimeout(id);
                   id = null;
                   if (isPingWorking) {
                     isPingWorking = false;
                     $("#cannot-ping").slideDown();
                   }
                 }
                 scheduleNextIdlePing();
               }});
  var id = window.setTimeout(
    function() {
      // This is our "real" success function: basically, if we
      // haven't received an error in IDLE_PING_DELAY ms, then
      // we should assume success and hide the #cannot-ping
      // element.
      if (id) {
        id = null;
        if (!isPingWorking) {
          isPingWorking = true;
          $("#cannot-ping").slideUp();
        }
      }
    }, IDLE_PING_DELAY);
}

function scheduleNextIdlePing() {
  window.setTimeout(sendIdlePing, IDLE_PING_DELAY);
}

$(window).ready(function() {
  if (window.location.protocol != "file:")
    scheduleNextIdlePing();
    documentName = $("#main-content h1:first").text();
  if (documentName.length > 0) {
    document.title = documentName + " - " + DOCUMENT_TITLE_ROOT;
  }
  else {
    document.title = DOCUMENT_TITLE_ROOT;
  }
  highlightCurrentPage();
  highlightCode();
})