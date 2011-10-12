
# Porting the Library Detector #

This example walks through the process of porting a XUL-based add-on to the
SDK. It's a very simple add-on and a good candidate for porting because
there are suitable SDK APIs for all its features. Even so, we have to make
small changes to the its user interface.

<img class="image-right" src="static-files/media/librarydetector/library-detector.png" alt="Library Detector Screenshot" />

The add-on is Paul Bakaus's
[Library Detector](https://addons.mozilla.org/de/firefox/addon/library-detector/).

The Library Detector tells you which JavaScript frameworks the current
web page is using. It does this by checking whether particular objects
that those libraries add to the global window object are defined.
For example, if `window.jQuery` is defined, then the page has loaded
[jQuery](http://jquery.com/).

For each library that it finds, the library detector adds an icon
representing that library to the status bar. It adds a tooltip to each
icon, which contains the library name and version.

You can browse and run the ported version in
[the Builder](https://builder.addons.mozilla.org/addon/1020373/revision/65/).

## How the Library Detector works ##

All the work is done inside a single file,
[`librarydetector.xul`](http://code.google.com/p/librarydetector/source/browse/trunk/chrome/content/librarydetector.xul)
This contains:

<ul>
	<li>a XUL overlay</li>
	<li>a script</li>
</ul>

The XUL overlay adds a `box` element to the browser's status bar:

<script type="syntaxhighlighter" class="brush: html"><![CDATA[
  &lt;statusbar id="status-bar"&gt; &lt;box orient="horizontal" id="librarydetector"&gt; &lt;/box&gt; &lt;/statusbar&gt;
]]>
</script>

The script does everything else.

The bulk of the script is an array of test objects, one for each library.
Each test object contains a function called `test`: if the
function finds the library, it defines various additional properties for
the test object, such as a `version` property containing the library version.
Each test also contains a `chrome://` URL pointing to the icon associated with
its library.

The script listens to [gBrowser](https://developer.mozilla.org/en/Code_snippets/Tabbed_browser)'s
`DOMContentLoaded` event. When this is triggered, the `testLibraries`
function builds an array of libraries by iterating through the tests and
adding an entry for each library which passes.

Once the list is built, the `switchLibraries` function constructs a XUL
`statusbarpanel` element for each library it found, populates it with the
icon at the corresponding `chrome://` URL, and adds it to the box.

Finally, it listen to gBrowser's `TabSelect` event, to update the contents
of the box for that window.

## Content Script Separation ##

The test objects in the original script need access to the DOM window object,
so in the SDK port, they need to run in a content script. In fact, they need
access to the un-proxied DOM window, so they can see the objects added by
libraries, so we’ll need to use the experimental
[unsafeWindow](dev-guide/addon-development/content-scripts/access.html) object.

`main.js` will use a [`page-mod`](packages/addon-kit/docs/page-mod.html)
to inject the content script into every new page.

The content script, which we'll call `library-detector.js`, will keep most of
the logic of the `test` functions intact. However, instead of maintaining its
own state by listening for `gBrowser` events and updating the
user interface, the content script will just run when it's loaded, collect
the array of library names, and post it back to `main.js`.

`main.js` responds to that message by fetching the tab
corresponding to that worker using `worker.tab`, and adding the array of
library names to that tab's `libraries` property.

The content script is executed once for every `window.onload` event, so
it will run multiple times when a single page containing multiple iframes
is loaded. So `main.js` needs to filter out any duplicates, in case
a page contains more than one iframe, and those iframes use the same library.

## Implementing the User Interface ##

The [`widget`](packages/addon-kit/docs/widget.html) module is a natural fit
for this add-on's UI. We'll want to specify its content using HTML, so we
can display an array of icons. The widget must be able to display different
content for different windows, so we'll use the
[`WidgetView`](packages/addon-kit/docs/widget.html) object.

`main.js` will create an array of icons corresponding to the array of library
names, and use that to build the widget's HTML content dynamically. It will
use the [`tabs`](packages/addon-kit/docs/tabs.html) module to update the
widget's content when necessary (for example, when the user switches between
tabs).

The XUL library detector displayed the detailed information about each
library on mouseover in a tooltip: we can't do this using a widget, so
instead will use a panel. We will need another content script in the
widget which listens for icon mouseover events and sends a message to
`main.js` containing the name of the corresponding library. `main.js`
handles this message by forwarding the library information on to the panel,
which updates its content.

<img class="image-center" src="static-files/media/librarydetector/panel-content.png" alt="Updating panel content" />
