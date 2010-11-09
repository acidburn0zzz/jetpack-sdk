The Jetpack SDK supports event-driven programming through its EventEmitter
framework. Jetpack modules emit events on state changes that might be of
interest to add-on code, such as: browser windows opening; pages loading;
network requests completing; mouse clicks. By registering a listener
function to an event emitter an add-on can receive notifications of these
events.

The interface exposed by an event emitter consists of two functions:

* **`on(type, listener)`**: register a listener
* **`removeListener(type, listener)`**: remove a listener

##Adding listeners##
You can add a listener to an event source by calling its `on(type, listener)`
function.

It takes two parameters:

* **`type`**: the type of event we are interested in, identified by a string.
Many event sources may emit more than one type of event: for example, a browser
window might emit both "open" and "close" events. The list of valid event types
is specific to an event emitter and is included with its documentation.

* **`listener`**: the listener itself. This is a function which will be called
whenever the event occurs. The arguments that will be passed to the listener
are specific to an event type and are documented with the event emitter.

For example, the following add-on registers two listeners with the
"private-browsing" module to listen for the "start" and "stop" events, and log
a string to the console reporting the change:

    var pb = require("private-browsing");

    pb.on("start", function() {
      console.log("Private browsing is on");
    });

    pb.on("stop", function() {
      console.log("Private browsing is off");
    });

It is not possible to enumerate the set of listeners for a given event.

<span class="aside">
In the examples I've tried this doesn't seem to be true. Also if we don't
want people using this in the listener we should not document it.
</span>
The value of `this` in the listener function is the event emitter instance on
which `on()` was called.

###Adding listeners in constructors###
Event emitters may be implemented at the module level, as is the case for the
"private-browsing" events, or they may be implemented by objects returned by
constructors.

In the latter case the objects typically define a property whose name is the
name of an event type prefixed with "on": for example, "onOpen", onReady" and
so on. Then in the object constructor the add-on developer can assign a
listener function to this property as an alternative to calling the object's
"on" function.

<span class="aside">
Either the example at [widget](#modules/addon-kit/widget) is wrong or I'm
confused. The example has only a single arg, which is the event. If it is wrong
I'll fix it...
</span>
For example: the [widget](#modules/addon-kit/widget) object generates an event
when the widget is clicked. The widget supplies two arguments to the listener:
the first is the widget itself and the second is a standard DOM event.

The following add-on creates a widget and assigns a listener to the
widget's `onClick` property in its constructor. The listener loads the Google
home page:

    var widgets = require("widget");

    widgets.add(widgets.Widget({
      label: "Widget with an image and a click handler",
      image: "http://www.google.com/favicon.ico",
      onClick: function(w, e) {
        e.view.content.location = "http://www.google.com";
      }
    }));

This is exactly equivalent to constructing the widget and then calling the
widget's `on("click", ..)` function:

    var widgets = require("widget");

    var widget = widgets.Widget({
      label: "Widget with an image and a click handler",
      image: "http://www.google.com/favicon.ico"
    });

    widget.on("click", function(w, e) {
      e.view.content.location = "http://www.google.com";
    });

    widgets.add(widget);

##Removing event listeners##
Event listeners can be removed by calling `removeListener(type, listener)`,
supplying the type of event and the listener to remove.

<span class="aside">
Will use a different example, maybe tabs, when they are updated to use on()
</span>
In the following add-on, we add two listeners to private-browsing's `start`
event, enter and exit private browsing, then remove the first listener and
enter private browsing again.

    var pb = require("private-browsing");

    function listener1() {
      console.log("Listener 1");
      pb.removeListener("start", listener1);
    }

    function listener2() {
      console.log("Listener 2");
    }

    pb.on("start", listener1);
    pb.on("start", listener2);

    pb.active=true;
    pb.active=false;
    pb.active=true;

Removing listeners is optional since they will be removed in any case
when the application or add-on is unloaded.

##Message events and the Worker object##
One particular type of event which is fundamental to Jetpack is the message
event. In Jetpack, add-ons which interact with web content are structured in
two parts:

* the main add-on code runs in the add-on process
* content scripts that interact with web content and run in the content process

These two parts communicate using a message-passing mechanism supplied by the
[worker](#modules/jetpack-code/content/worker) module, which is an event
emitter that emits two event types:
a "message" event and an "error" event. Thus an add-on can receive messages
from a content script by adding a listener to the worker's `on("message",...)`
function.

For example, the [page-mod](#modules/addon-kit/page-mod) module provides a
mechanism to execute scripts in the context of selected web pages. These
scripts are content scripts.

When a content script is attached to a page the
page mod emits the `on("attach")` event, which will supply a `worker` object
to any event listener. If the user of page-mod adds a listener to this worker
object, then it will receive messages from the associated content script.

The following add-on creates a page mod object which will execute the script
`postMessage(window.location.toString());` in the context of every page loaded.
The add-on assigns two event listeners:

* the first listens to the on("attach") event generated by the page mod, and
uses this event to get the worker object associated with the content script

* the second listens to the on("message") event generated by the worker, and
just logs the message to the console

The effect is that all messages from the content script are logged to the
console.

    var pageMod = require("page-mod");

    var myPageMod = pageMod.add({
      include: ['*'],
      contentScriptWhen: 'ready',
      contentScript: 'postMessage(window.location.toString());',
      onAttach: function onAttach(worker, mod) {
      worker.on('message', function(data) {
          console.log(data);
        });
      }
    });

The next section provides much more detail on [interacting with web
content](#guide/web-content) using content scripts.
