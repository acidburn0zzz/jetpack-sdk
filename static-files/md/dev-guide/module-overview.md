We've already seen that the JavaScript modules provided by the SDK are CommonJS
modules and that they are collected into CommonJS packages. There are two main
packages:

* the ***[addon-kit](#package/addon-kit)*** package provides high-level APIs
for add-on developers. Most of the needs of most developers should be served
by the modules found here, and the bulk of this guide is dedicated to modules
from this package. Modules in this packages also don't require any special
privileges to run.

* the ***[jetpack-core](#package/jetpack-core)*** package provides low-level
APIs. Most of the modules it contains are intended for people writing certain
specific types of add-ons, and for people writing their own reusable modules.
In particular it contains modules that supply basic services, like messaging,
for higher-level modules. Many of the modules in this package require
privileged access to the browser chrome. Working with these modules is
documented more extensively in the [Internals Guide](#guide/internals).

In this section we will first summarize some of the common idioms used by SDK
modules, then look at how you can use the modules to build various parts of
your add-on.

## Add-on SDK idioms ##

### Naming conventions ###
SDK module names are all lower case. Where a module name contains more than
one word, the words are separated using dashes:

    addon-module

SDK function names, property names and variable names are all CamelCase
with a lower case initial letter. Object constructors are CamelCase with an
upper case initial letter:

    addOnFunction
    AddOnObject

### Constructors ###
Many SDK modules export constructors that create object instances for use
by add-on code.

The constructor takes a single argument: this is an anonymous object called
`options` which is typically supplied to the constructor as an object literal
listing values for named object properties. So you will generally see objects
constructed using the following pattern:

    var addOnModule = require("addon-module");

    var myAddOnObject = new sdkModule.AddOnObject({
      property1: value1,
      property2: value2
    });

### Events ###
The SDK supports event-driven programming through its Event Emitter framework.
Objects which integrate Event Emitter functions can emit events such as pages
loading, windows opening and user interactions.

Add-on developers can assign listeners to these events and are then notified
when they occur. Event listeners can be added using the `on(type, listener)`
function and removed using the `removeListener(type, listener)` function:

    function handleEvent() {
      // Handle the event here
    }

    addOnEventEmitter.on("event", handleEvent());

    addOnEventEmitter.removeListener("event", handleEvent());

For a more comprehensive account of events see the Developer Guide's
[Events](#guide/events) section.

### Content scripting ###
Several modules need to interact directly with web content, either web content
they host themselves (such as the [panel](#modules/panel) module) or web
content hosted by the browser (such as the [page-mode](#modules/page-mod)).

These modules follow a common pattern in which the code
that actually interacts with the content is executed as a separate script
called a content script. The content script and the main add-on script
communicate using an asynchronous message-passing mechanism.

Objects that implement this scheme include properties that specify which
content scripts should be run and when:

    var myAddOnObject = new addOnModule.AddOnObject({
      contentScriptWhen: "ready",
      contentScript: "window.alert('Page loaded')",
      contentScriptURL: "[data.url("content-script.js")]"
      }
    });

For a more comprehensive account of content scripts see the Developer Guide's
[Content Scripting](#guide/content-scripting) section.

## SDK module functionality ##

### Globals ###
For full information on the globals available to Add-on code, see
the [Globals](#guide/globals) appendix.

* ***JavaScript globals***: all SDK code has access to the globals defined
in [JavaScript
1.8.1](https://developer.mozilla.org/En/New_in_JavaScript_1.8.1) such as
`Math`, `Array` and `JSON`.

* ***CommonJS globals***: SDK code also has access to `require` and `exports`
as specified by version 1.0 of the [CommonJS Module 
Specification](http://wiki.commonjs.org/wiki/Modules/1.0).

* ***Add-on SDK globals***: the Add-on SDK defines a number of globals, the
most widely used of which is probably the `console` global. This object allows
you to log messages to the console (standard output in the default
implementation):

        console.log("A message");

### Building a UI ###
The SDK provides four modules to help the add-on developer create a UI:

* ***[widget](#module/addon-kit/widget)***: a widget is permanently displayed
in a dedicated bar in the browser chrome. It may contain HTML content or an
image, and can notify the add-on code when the user interacts with it, for
example by clicking it. 
A widget is a good choice for displaying content that
should always be visible to the user, or to provide a way to access other parts
of an add-on's user interface: for example a widget might open a settings
dialog when the user clicks it.

* ***[panel](#module/addon-kit/panel)***: a panel is a dialog. It persists
until dismissed by the user or a program, but will be hidden if the user
interacts with other parts of the browser or another application. A panel may
contain HTML content and can notify the add-on when the user interacts with it.
A panel can also be supplied with [content
scripts](#guide/working-with-content-scripts) which interact with the content
hosted by the panel.
A panel is a good choice for displaying transient parts of a user interface.

* ***[context-menu](#module/addon-kit/panel)***: the context-menu module
provides a mechanism to add items and submenus to the browser's context menu.

* ***[notifications](#module/addon-kit/notifications)***: this module enables
an add-on to display transient messages to the user.

###Interacting with the Web###
* ***[page-mod](#module/addon-kit/page-mod)***: this module enables you to
execute content scripts in the context of selected web pages, effectively
rewriting the pages on the fly.

* ***[page-worker](#module/addon-kit/page-mod)***: using a page worker an
add-on can can load a page and access its content without displaying it to
the user.

* ***[request](#module/addon-kit/request)***: the request module enables you
to make HTTP GET and POST requests from your add-on.

###Interacting with the system###
* ***[clipboard](#module/addon-kit/clipboard)***: get and set the contents of
the system clipboard

* ***[private-browsing](#module/addon-kit/private-browsing)***: get notified
about transitioning into/out of private browsing mode, and also start or stop
private browsing mode. You should use this module if your add-on records
anything which should not be recorded in private browsing mode, such as the
Web sites visited by the user.

* ***[selection](#module/addon-kit/selection)***: get and set any selection
in the active page, either as text or HTML.

* ***[tabs](#module/addon-kit/tabs)***: get the list of open tabs,
the current active tab, and get notified of changes to these. Retrieve each tab
and get certain information about it. Open new tabs. Note that you can't access
the content hosted by the tab using this API.

* ***[windows](#module/addon-kit/windows)***: get the list of open windows,
the current active window, and get notified of changes to these. Retrieve each
window and get certain information about it. Open new windows. Again: you
can't access the content hosted by the window using this API.

###Utilities
<span class="aside">
This module needs much better documentation.
</span>

* ***[localization](#module/addon-kit/localization)***: helps you to support
multiple language variants for your add-on without needing to bundle localized
strings for all the languages with the add-on itself.

* ***[storage](#module/addon-kit/storage)***: provides your add-on with
persistent storage.

* ***[self](#module/jetpack-core/self)***: access to your add-on's [Program
ID](#guide/implementing) and any data bundled with your add-on: for example,
HTML content to be displayed in a user interface component or a content
script. Note that this module is in the 
[jetpack-core](#package/jetpack-core) package.

Next we will take a more detailed look at one of the basic idioms in the SDK:
the [Event Emitter framework](#guide/working-with-events).