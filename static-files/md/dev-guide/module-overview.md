This section of the tutorial provides an overview of the modules supplied by
the add-on SDK.

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
Modules that access with web content follow a common pattern in which the code
that actually interacts with the content is executed as a separate script
called a content script. The content script and the main add-on script
communicate using an asynchronous message-passing mechanism.

Classes that implement this scheme include properties that specify which
content scripts should be run and when:

    var myAddOnObject = new addOnModule.AddOnObject({
      contentScriptWhen: "ready",
      contentScript: "window.alert('Page loaded')",
      contentScriptURL: "[data.url("content-script.js")]"
      }
    });

For a more comprehensive account of content scripts see the Developer Guide's
[Interacting with Web Content](#guide/web-content) section.

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
