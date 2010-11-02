This section of the tutorial provides an overview of the modules supplied by
Jetpack to support add-on development.

## Globals ##
For full information on the globals available to Jetpack code, see
the [Jetpack Globals] appendix.

### JavaScript Globals ###
All Jetpack code has access to the globals defined in [JavaScript 
1.8.1](https://developer.mozilla.org/En/New_in_JavaScript_1.8.1) such as
`Math`, `Array` and `JSON`.

### CommonJS Globals ###
Jetpack code also has access to `require` and `exports` as specified by
version 1.0 of the [CommonJS Module 
Specification](http://wiki.commonjs.org/wiki/Modules/1.0).

### Jetpack Globals ###
Jetpack defines a number of globals, the most widely -used of which is
probably the `console` global. This object allows you to log messages to the
console.

    console.log("A message");

The default implementation of the console writes messages to standard output.

## Common idioms ##

### Naming conventions ###
Jetpack module names are all lower case. Where a module name contains more than
one word, the words are separated using dashes:

    jetpack-module

Jetpack function names, property names and variable names are all CamelCase
with a lower case initial letter. Object constructors are CamelCase with an
upper case initial letter:

    jetpackFunction
    JetpackObject

### Object construction ###
Many Jetpack modules expose their functionality through objects. A common
pattern for such a module is to export just three functions:

* a constructor for an object
* an `add` function which activates the object
* a `remove` function which deactivates the object

The constructor takes a single argument: this is an anonymous object called
`options` which is typically supplied to the constructor as an object literal
listing values for named object properties. So you will generally see objects
constructed using the following pattern:

    var jetPackModule = require("jetpack-module");

    var myJetpackObject = new jetPackModule.JetpackObject({
      property1: value1,
      property2: value2
    }) 

### Events ###
If the object generates events then it will have a property that can be
assigned to a callback function which will be called when the event happens.
Properties like this are generally named with the capitalized name of the
event prefixed with "on" (for example, "onMessage", "onError", "onAttach").
For example, if the object generates an error event we might construct it like
this:

    var myJetpackObject = new jetPackModule.JetpackObject({
      property1: value1,
      onError: function logError(message) {
        console.log(message);
      }
    })

For a more comprehensive account of events see the Developer Guide's
[Events](#guide/events) section.



