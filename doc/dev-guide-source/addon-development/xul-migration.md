
# XUL Migration Guide #

This guide aims to help you migrate a traditional XUL-based add-on
to the SDK.

First, we'll look at the benefits and limitations of using the SDK,
to help decide whether your add-on is a good candidate
for porting.

Next, we'll look at some of the main tasks involved in migrating
to the SDK:

* working with content scripts
* using the SDK's [supported APIs](packages/addon-kit/addon-kit.html)
* how to go beyond the SDK's supported APIs when necessary, by using
[third party modules](dev-guide/addon-development/third-party-modules.html)
or using the SDK's [low-level APIs](packages/addon-kit/api-utils.html) to
perform dynamic XUL manipulation or to access XPCOM objects directly.

Finally, we'll walk through a simple example.

## Should You Migrate? ##

The benefits and limitation of the SDK development compared to XUL development
are summarized [here](dev-guide/addon-development/sdk-vs-xul.html).

Whether you should migrate a particular add-on is largely a matter of
how well the SDK's supported APIs meet its needs.

* If your add-on can accomplish everything it needs using only the
supported APIs, it's a good candidate for migration.

* If your add-on needs a lot of help from the low-level APIs, then you
won't see much benefit from migrating.

* If your add-on needs a fairly limited amount of help from low-level
APIs, then it might still be worth migrating: we'll add more supported
APIs in future releases to meet important use cases, and eventually hope
to have a comprehensive collection of third party modules filling many of
the gaps.

## Content Scripts ##

In a XUL-based add-on, code that uses XPCOM objects, code that manipulates
the browser chrome, and code that interacts with web pages all runs in the
same context. But the SDK makes a distinction between:

* **add-on scripts**, which can use the SDK APIs, but are not able to interact
with web pages
* **content scripts**, which can access web pages, but do not have access to
the SDK's APIs

Content scripts and add-on scripts communicate by sending each other JSON
messages: in fact, the ability to communicate with the add-on scripts is the
only extra privilege a content script is granted over a normal remote web
page script.

So, for example, suppose an add-on wants to make a cross-domain XMLHttpRequest
based on some data extracted from a web page. In a XUL-based extension you
would implement all this in a single script. An SDK-based add-on would need
to be structured like this:

* the main add-on code attaches a content script to the page, and registers
a listener function for messages from the content script
* the content script extracts the data from the page and sends it to the
main add-on code in a message
* the main add-on code receives the message and sends the request.

<img class="image-center" src="static-files/media/xul-migration-cs.png"
alt="Content script organization">

A XUL-based add-on will need to be reorganized to respect this distinction.

This design is motivated by two related concerns. First is security: it
reduces the risk that a malicious web page will be able to access privileged
APIs. Second is the need to be compatible with the multi-process architecture
planned for Firefox and already partly implemented in Firefox Mobile. Note
that all mobile add-ons already need to use
[a similar design](https://wiki.mozilla.org/Mobile/Fennec/Extensions/Electrolysis).

There's much more information on content scripts in the
[Working With Content Scripts](dev-guide/addon-development/web-content.html) guide.

## Using the SDK's "supported" APIs ##

See this
[quick overview](dev-guide/addon-development/api-modules.html) and
[links to detailed API documentation](packages/addon-kit/addon-kit.html).
If the supported APIs do what you need, they're the best option: you get the
benefit of compatibility across Firefox releases, and of the SDK's security
model.

APIs like [`widget`](packages/addon-kit/docs/widget.html) and
[`panel`](packages/addon-kit/docs/panel.html) are very generic, and with the
right content can be used to replace many specific XUL elements. But there are
some notable limitations in the SDK APIs, and even a fairly simple UI may need
some degree of redesign to work with them. In particular:

* widgets always appear by default in the
[add-on bar](https://developer.mozilla.org/en/The_add-on_bar),
although users may relocate them by
[toolbar customization](http://support.mozilla.com/en-US/kb/how-do-i-customize-toolbars)
* there's currently no way to add items to the browser's main menus using the
SDK's supported APIs.

These are intentional design choices, the belief being that it makes for a
better user experience for add-ons to expose their interfaces in a consistent
way. So it's worth considering changing your user interface to align with the
SDK APIs.

Having said that, add-ons which make drastic changes to the browser chrome
will very probably need more than the SDK's supported APIs can offer.

Similarly, the supported APIs expose only a small fraction of the full range
of XPCOM functionality.

## Third Party Modules ##

See the
[guide to using third party modules](dev-guide/addon-development/third-party-modules.html).
If you can find a third party module to do what you want, this is a great way
to use features not supported in the SDK without having to use the low-level
APIs.

Note that by using third party modules you're likely to lose the security and
compatibility benefits of using the SDK.

## The "low-level" APIs ##

If you can't find a suitable third party module you can support, you can use
low-level APIs to:

* load and access any XPCOM component
* modify the browser chrome using dynamic manipulation of the XUL
* directly access the [tabbrowser](https://developer.mozilla.org/en/XUL/tabbrowser)
object

All these techniques involve the use of low-level APIs, which don't have
the same compatibility guarantees as the supported APIs.

### Using XPCOM ###

To use XPCOM, you need use `require("chrome")`, which gives you
direct access to the
[`Components`](https://developer.mozilla.org/en/Components_object) object.

<div class="warning">
If a module which uses <code>require("chrome")</code>
is compromised, the attacker gets full access to the browser's capabilities
</div>

The following complete add-on uses
[`nsIPromptService`](https://developer.mozilla.org/en/XPCOM_Interface_Reference/nsIPromptService)
to display an alert dialog:

    var {Cc, Ci} = require("chrome");

    var promptSvc = Cc["@mozilla.org/embedcomp/prompt-service;1"].
                    getService(Ci.nsIPromptService);

    var widget = require("widget").Widget({
      id: "xpcom example",
      label: "Mozilla website",
      contentURL: "http://www.mozilla.org/favicon.ico",
      onClick: function() {
        promptSvc.alert(null, "My Add-on", "Hello from XPCOM");
      }
    });

It's good practice to encapsulate code which uses XPCOM by
[packaging it in its own module](dev-guide/addon-development/implementing-reusable-module.html).
For example, we could package the alert feature implemented above using a
script like:

    var {Cc, Ci} = require("chrome");

    var promptSvc = Cc["@mozilla.org/embedcomp/prompt-service;1"].
                getService(Ci.nsIPromptService);

    exports.alert = function(title, text) {
        promptSvc.alert(null, title, text);
    };

If we save this as "prompt.js" in our add-on's `lib` directory, we can rewrite
`main.js` to use it as follows:

    var widget = require("widget").Widget({
      id: "xpcom example",
      label: "Mozilla website",
      contentURL: "http://www.mozilla.org/favicon.ico",
      onClick: function() {
        require("prompt").alert("My Add-on", "Hello from XPCOM");
      }
    });

One of the benefits of this is that we can control which parts of the add-on
are granted chrome privileges, making it easier to review and secure the code.

### window-utils ###

The [`window-utils`](packages/api-utils/docs/window-utils.html) module gives
you direct access to the browser chrome.

Here's a really simple example add-on that modifies the browser chrome using
the [`window-utils`](packages/api-utils/docs/window-utils.html) module:

    var windowUtils = require("window-utils");

    windowUtils = new windowUtils.WindowTracker({
      onTrack: function (window) {
        if ("chrome://browser/content/browser.xul" != window.location) return;
      var forward = window.document.getElementById('forward-button');
      var parent = window.document.getElementById('unified-back-forward-button');
      parent.removeChild(forward);
      }
    });

This example just removes the 'forward' button from the browser. It constructs
a `WindowTracker` object and assigns a function to the constructor's `onTrack`
option. This function will be called whenever a window is opened. The function
checks whether the window is the browser's XUL, and if it is, uses
DOM manipulation functions to modify it.

There are more useful examples of this technique in the Jetpack Wiki's
collection of [third party modules](https://wiki.mozilla.org/Jetpack/Modules).

### tab-browser ###

The [`tab-browser`](packages/api-utils/docs/tab-browser.html) module gives
you direct access to the
[tabbrowser](https://developer.mozilla.org/en/XUL/tabbrowser) object.

This simple example modifies the selected tab's CSS to enable the user to
highlight the selected tab:

    var widgets = require("widget");
    var tabbrowser = require("tab-browser");
    var self = require("self");

    function highlightTab(tab) {
      if (tab.style.getPropertyValue('background-color')) {
        tab.style.setProperty('background-color','','important');
      }
      else {
        tab.style.setProperty('background-color','rgb(255,255,100)','important');
      }
    }

    var widget = widgets.Widget({
      id: "tab highlighter",
      label: "Highlight tabs",
      contentURL: self.data.url("highlight.png"),
      onClick: function() {
        highlightTab(tabbrowser.activeTab);
      }
    });

## An Example: Porting the Library Detector ##


