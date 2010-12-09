## Constructors ##

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

## [Events](#guide/events) ##

The SDK supports event-driven programming through its [`Event
Emitter`](#module/jetpack-core/events) framework.
Objects which integrate Event Emitter functions can emit events such as pages
loading, windows opening and user interactions.

Add-on developers can assign listeners to these events and are then notified
when they occur.

## [Content Scripting](#guide/web-content) ##

Several modules need to interact directly with web content, either web content
they host themselves (such as the [`panel`](#module/addon-kit/panel) module) or
web content hosted by the browser (such as the 
[`page-mod`](#module/addon-kit/page-mod)).

These modules follow a common pattern in which the code
that actually interacts with the content is executed as a separate script
called a content script. The content script and the main add-on script
communicate using an asynchronous message-passing mechanism.

Objects that implement this scheme include properties that specify which
content scripts should be run and when.

<br>
**Next**: [building a UI](#guide/api-ui).