
<!-- This Source Code Form is subject to the terms of the Mozilla Public
   - License, v. 2.0. If a copy of the MPL was not distributed with this
   - file, You can obtain one at http://mozilla.org/MPL/2.0/. -->

<!-- contributed by Nickolay Ponomarev [asqueella@gmail.com] -->
<!-- contributed by Myk Melez [myk@mozilla.org] -->
<!-- contributed by Irakli Gozalishvil [gozala@mozilla.com] -->

The `page-mod` module enables you to run scripts in the context of
specific web pages. To use it, you specify:

* one or more scripts to attach. The SDK calls scripts like this
"content scripts". For all the details on content scripts, see the
[guide to content scripts](dev-guide/guides/content-scripts/index.html).
* a pattern that a page's URL must match, in order for the script(s)
to be attached to that page

For example, the following add-on displays an alert whenever the user
visits any page hosted at "mozilla.org":

    var pageMod = require("page-mod");
    pageMod.PageMod({
      include: "*mozilla.org",
      contentScript: 'window.alert("Page matches ruleset");'
    });

You can modify the page in your script:

    var pageMod = require("page-mod");
    pageMod.PageMod({
      include: "*mozilla.org",
      contentScript: 'document.body.innerHTML = ' +
                     ' "<h1>Page matches ruleset</h1>";'
    });

You can supply the content script(s) in one of two ways:

* as a string literal, or an array of string literals, assigned to the `contentScript` option, as above
* as separate files supplied in your add-on's "data" directory, assigning
the filename, or array of filenames, to the `contentScriptFile` option:

<!-- -->

<span class="aside">
In these examples we're using the
[`self`](packages/addon-kit/self.html) module to retrieve a URL pointing
to the file.</span>

    var data = require("self").data;
    var pageMod = require("page-mod");
    pageMod.PageMod({
      include: "*.org",
      contentScriptFile: data.url("my-script.js")
    });

<!-- -->

    var data = require("self").data;
    var pageMod = require("page-mod");

    pageMod.PageMod({
      include: "*.mozilla.org",
      contentScriptFile: [self.data.url("jquery-1.7.min.js"),
                          self.data.url("my-script.js")]
    });

<div class="warning">
<p>Unless your content script is extremely simple and consists only of a
static string, don't use <code>contentScript</code>: if you do, you may
have problems getting your add-on approved on AMO.</p>
<p>Instead, keep the script in a separate file and load it using
<code>contentScriptFile</code>. This makes your code easier to maintain,
secure, debug and review.</p>
</div>

## Communicating With the Content Scripts ##

Your add-on's "main.js" can't directly access the state of content scripts
you load, but you can communicate between your add-on and its content scripts
by exchanging messages.

To do this, you'll need to listen to the page-mod's `attach` event.
This event is triggered every time the page-mod's content script is attached
to a page. The listener is passed a `worker` object that your add-on can use
to send and receive messages.

For example, this add-on retrieves the HTML content of specific tags from
pages that match the pattern.

main.js:

    var tag = "p";
    var data = require("self").data;
    var pageMod = require("page-mod");

    pageMod.PageMod({
      include: "*.mozilla.org",
      contentScriptFile: data.url("element-getter.js"),
      onAttach: function(worker) {
        worker.port.emit("getElements", tag);
        worker.port.on("gotElement", function(elementContent) {
          console.log(elementContent);
        });
      }
    });

element-getter.js:

    self.port.on("getElements", function(tag) {
      var elements = document.getElementsByTagName(tag);
      for (var i = 0; i < elements.length; i++) {
        self.port.emit("gotElement", elements[i].innerHTML);
      }
    });

When the user loads a page hosted at "mozilla.org":

<img class="image-right" alt="page-mod messaging diagram" src="static-files/media/page-mod-messaging.png"/>

* The content script "element-getter.js" is attached to the page
and runs. It adds a listener to the `getElements` message.
* The `attach` event is sent to the "main.js" code. Its event handler sends
the `getElements` message to the content script, and then adds a listener
to the `gotElement` message.
* The content script receives the `getElements` message, retrieves all
elements of that type, and for each element sends a `gotElement` message
containing the element's `innerHTML`.
* The "main.js" code receives each `gotElement` message and logs the
contents.

If multiple matching pages are loaded then each page is loaded into its
own execution context with its own copy of the content scripts. In this
case `onAttach` is called once for each loaded page, and the add-on code
will have a separate worker for each page.

### Mapping Workers to Tabs ###

The `worker` has a `tab` property which returns the tab associated with
this worker. You can use this to access
the [`tabs API`](packages/addon-kit/tabs.html) for the tab associated
with a specific page:

    var pageMod = require("page-mod");
    var tabs = require("tabs");

    pageMod.PageMod({
      include: ["*"],
      onAttach: function onAttach(worker) {
        console.log(worker.tab.title);
      }
    });

To learn much more about communicating with content scripts, see the
[guide to content scripts](dev-guide/guides/content-scripts/index.html) and in
particular the chapter on
[communicating using `port`](dev-guide/guides/content-scripts/using-port.html).


<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

















A page mod does not modify its pages until those pages are loaded or reloaded.
In other words, if your add-on is loaded while the user's browser is open, the
user will have to reload any open pages that match the mod for the mod to affect
them.

To stop a page mod from making any more modifications, call its `destroy`
method.

<div class="warning">
  Starting with SDK 1.11, page-mod only attaches scripts to documents loaded
  in tabs. It will not attach scripts to add-on panels, page-workers, widgets,
  or  Firefox hidden windows.
</div>

### Styling web pages ###

Sometimes adding a script to web pages is not enough, you also want to style
them. `PageMod` provides an easy way to do that through options' `contentStyle`
and `contentStyleFile` properties:

    var data = require("self").data;
    var pageMod = require("page-mod");

    pageMod.PageMod({
      include: "*.org",

      contentStyleFile: data.url("my-page-mod.css"),
      contentStyle: [
        "div { padding: 10px; border: 1px solid silver}",
        "img { display: none}"
      ]
    })

`PageMod` will add these styles as
[user style sheets](https://developer.mozilla.org/en/CSS/Getting_Started/Cascading_and_inheritance).

#### Working with Relative URLs in CSS Rules ####

You can't currently use relative URLs in style sheets loaded in this way.
For example, consider a CSS file that references an external file like this:

    background: rgb(249, 249, 249) url('../../img/my-background.png') repeat-x top center;

If you attach this file using `contentStyleFile`, "my-background.png"
will not be found.

As a workaround for this, you can build an absolute URL to a file in your
"data" directory, and construct a `contentStyle` option embedding that URL
in your rule. For example:

    var data = require("self").data;

    var pageMod = require("page-mod").PageMod({
      include: "*",
      contentStyleFile: data.url("my-style.css"),
      // contentStyle is built dynamically here to include an absolute URL
      // for the file referenced by this CSS rule.
      // This workaround is needed because we can't use relative URLs
      // in contentStyleFile or contentStyle.
      contentStyle: "h1 { background: url(" + data.url("my-pic.jpg") + ")}"
    });

This add-on uses a separate file "my-style.css", loaded using
`contentStyleFile`, for all CSS rules except those that reference
an external file. For the rule that needs to refer to "my-pic.jpg",
which is stored in the add-on's "data" directory, it uses `contentStyle`.

Dynamically constructing code strings like those assigned to `contentScript`
or `contentStyle` is usually considered an unsafe practice that may cause an
add-on to fail AMO review. In this case it is safe, and should be allowed,
but including a comment like that in the example above will help to
prevent any misunderstanding.

## Communicating With Content Scripts ##

When a matching page is loaded the `PageMod` will call the function that the
add-on code supplied to `onAttach`. The `PageMod` supplies one argument to
this function: a `worker` object.

The [`worker`](packages/api-utils/content/worker.html) can be thought of as
the add-on's end of a communication channel between the add-on code and
the content scripts that have been attached to this page.

Thus the add-on can pass messages to the content scripts by calling the
worker's `postMessage` function and can receive messages from the content
scripts by registering a function as a listener to the worker's `on` function.

Note that if multiple matching pages are loaded simultaneously then each page
is loaded into its own execution context with its own copy of the content
scripts. In this case `onAttach` is called once for each loaded page, and the
add-on code will have a separate worker for each page:

![Multiple workers](static-files/media/multiple-workers.jpg)

This is demonstrated in the following example:

    var pageMod = require("page-mod");
    var tabs = require("tabs");

    var workers = [];

    pageMod.PageMod({
      include: ["http://www.mozilla*"],
      contentScriptWhen: 'end',
      contentScript: "onMessage = function onMessage(message) {" +
                     "  window.alert(message);};",
      onAttach: function onAttach(worker) {
        if (workers.push(worker) == 3) {
          workers[0].postMessage("The first worker!");
          workers[1].postMessage("The second worker!");
          workers[2].postMessage("The third worker!");
        }
      }
    });

    tabs.open("http://www.mozilla.com");
    tabs.open("http://www.mozilla.org");
    tabs.open("http://www.mozilla-europe.org");

Here we specify a ruleset to match any URLs starting with
"http://www.mozilla". When a page matches we add the supplied worker to
an array, and when we have three workers in the array we send a message to
each worker in turn, telling it the order in which it was attached. The
worker just displays the message in an alert box.

This shows that separate pages execute in separate contexts and that each
context has its own communication channel with the add-on script.

Note though that while there is a separate worker for each execution context,
the worker is shared across all the content scripts associated with a single
execution context. In the following example we pass two content scripts into
the `PageMod`: these content scripts will share a worker instance.

In the example each content script identifies itself to the add-on script
by sending it a message using the global `postMessage` function. In the
`onAttach` function the add-on code logs the fact that a new page is
attached and registers a listener function that simply logs the message:


    var pageMod = require("page-mod");
    var data = require("self").data;
    var tabs = require("tabs");

    pageMod.PageMod({
      include: ["http://www.mozilla*"],
      contentScriptWhen: 'end',
      contentScript: ["postMessage('Content script 1 is attached to '+ " +
                      "document.URL);",
                      "postMessage('Content script 2 is attached to '+ " +
                      "document.URL);"],
      onAttach: function onAttach(worker) {
        console.log("Attaching content scripts")
        worker.on('message', function(data) {
          console.log(data);
        });
      }
    });

    tabs.open("http://www.mozilla.com");

The console output of this add-on is:

<pre>
  info: Attaching content scripts
  info: Content script 1 is attached to http://www.mozilla.com/en-US/
  info: Content script 2 is attached to http://www.mozilla.com/en-US/
</pre>


### Attaching content scripts to tabs ###

We've seen that the page mod API attaches content scripts to pages based on
their URL. Sometimes, though, we don't care about the URL: we just want
to execute a script on demand in the context of a particular tab.

For example, we might want to run a script in the context of the currently
active tab when the user clicks a widget: to block certain content, to
change the font style, or to display the page's DOM structure.

Using the `attach` method of the [`tab`](packages/addon-kit/tabs.html)
object, you can attach a set of content scripts to a particular tab. The
scripts are executed immediately.

The following add-on creates a widget which, when clicked, highlights all the
`div` elements in the page loaded into the active tab:

    var widgets = require("widget");
    var tabs = require("tabs");

    var widget = widgets.Widget({
      id: "div-show",
      label: "Show divs",
      contentURL: "http://www.mozilla.org/favicon.ico",
      onClick: function() {
        tabs.activeTab.attach({
          contentScript:
            'var divs = document.getElementsByTagName("div");' +
            'for (var i = 0; i < divs.length; ++i) {' +
              'divs[i].setAttribute("style", "border: solid red 1px;");' +
            '}'
        });
      }
    });

## Destroying Workers ##

Workers generate a `detach` event when their associated page is closed: that
is, when the tab is closed or the tab's location changes. If
you are maintaining a list of workers belonging to a page mod, you can use
this event to remove workers that are no longer valid.

For example, if you maintain a list of workers attached to a page mod:

    var workers = [];

    var pageMod = require("page-mod").PageMod({
      include: ['*'],
      contentScriptWhen: 'ready',
      contentScriptFile: data.url('pagemod.js'),
      onAttach: function(worker) {
        workers.push(worker);
      }
    });

You can remove workers when they are no longer valid by listening to `detach`:

    var workers = [];

    function detachWorker(worker, workerArray) {
      var index = workerArray.indexOf(worker);
      if(index != -1) {
        workerArray.splice(index, 1);
      }
    }

    var pageMod = require("page-mod").PageMod({
      include: ['*'],
      contentScriptWhen: 'ready',
      contentScriptFile: data.url('pagemod.js'),
      onAttach: function(worker) {
        workers.push(worker);
        worker.on('detach', function () {
          detachWorker(this, workers);
        });
      }
    });

<api name="PageMod">
@class
A PageMod object. Once activated a page mod will execute the supplied content
scripts in the context of any pages matching the pattern specified by the
'include' property.
<api name="PageMod">
@constructor
Creates a PageMod.
@param options {object}
  Options for the PageMod, with the following keys:
  @prop include {string,array}
    A match pattern string or an array of match pattern strings.  These define
    the pages to which the PageMod applies.  See the
    [match-pattern](packages/api-utils/match-pattern.html) module for
    a description of match pattern syntax.
    At least one match pattern must be supplied.

  @prop [contentScriptFile] {string,array}
    The local file URLs of content scripts to load.  Content scripts specified
    by this option are loaded *before* those specified by the `contentScript`
    option. Optional.
  @prop [contentScript] {string,array}
    The texts of content scripts to load.  Content scripts specified by this
    option are loaded *after* those specified by the `contentScriptFile` option.
    Optional.
  @prop [contentScriptWhen="end"] {string}
    When to load the content scripts. This may take one of the following
    values:

    * "start": load content scripts immediately after the document
    element for the page is inserted into the DOM, but before the DOM content
    itself has been loaded
    * "ready": load content scripts once DOM content has been loaded,
    corresponding to the
    [DOMContentLoaded](https://developer.mozilla.org/en/Gecko-Specific_DOM_Events)
    event
    * "end": load content scripts once all the content (DOM, JS, CSS,
    images) for the page has been loaded, at the time the
    [window.onload event](https://developer.mozilla.org/en/DOM/window.onload)
    fires

    This property is optional and defaults to "end".
  @prop [contentScriptOptions] {object}
    Read-only value exposed to content scripts under `self.options` property.

    Any kind of jsonable value (object, array, string, etc.) can be used here.
    Optional.

  @prop [contentStyleFile] {string,array}
    The local file URLs of stylesheet to load. Content style specified by this
    option are loaded *before* those specified by the `contentStyle` option.
    Optional.
  @prop [contentStyle] {string,array}
    The texts of stylesheet rules to add. Content styles specified by this
    option are loaded *after* those specified by the `contentStyleFile` option.
    Optional.

  @prop [attachTo] {string,array}
    Option to specify on which documents PageMod should be applied.
    It accepts following values:

    * "existing": the PageMod will be automatically applied on already opened
    tabs.
    * "top": the PageMod will be applied to top-level tab documents
    * "frame": the PageMod will be applied to all iframe inside tab documents

    When omitted, it defaults to ["top", "frame"]. When set, you have to at
    least set either "top" and/or "frame".
    Optional.

  @prop [onAttach] {function}
A function to call when the PageMod attaches content scripts to
a matching page. The function will be called with one argument, a `worker`
object which the add-on script can use to communicate with the content scripts
attached to the page in question.

</api>

<api name="include">
@property {List}
A [list](packages/api-utils/list.html) of match pattern strings.  These
define the pages to which the page mod applies.  See the
[match-pattern](packages/api-utils/match-pattern.html) module for a
description of match patterns. Rules can be added to the list by calling its
`add` method and removed by calling its `remove` method.

</api>

<api name="destroy">
@method
Stops the page mod from making any more modifications.  Once destroyed the page
mod can no longer be used.  Note that modifications already made to open pages
will not be undone, except for any stylesheet added by `contentStyle` or
`contentStyleFile`, that are unregistered immediately.
</api>

<api name="attach">
@event
This event is emitted this event when the page-mod's content scripts are
attached to a page whose URL matches the page-mod's `include` filter.

@argument {Worker}
The listener function is passed a [`Worker`](packages/api-utils/content/worker.html) object that can be used to communicate
with any content scripts attached to this page.
</api>

<api name="error">
@event
This event is emitted when an uncaught runtime error occurs in one of the page
mod's content scripts.

@argument {Error}
Listeners are passed a single argument, the
[Error](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Error)
object.
</api>

</api>
