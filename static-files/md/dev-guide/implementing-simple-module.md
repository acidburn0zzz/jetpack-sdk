For a very simple add-on it's probably appropriate to keep all the code in a
single "main.js" module. But for an add-on of any size or complexity you are
likely to want to factor common code into separate modules so they are usable
by different parts of your add-on or even by other programs.

In this example we'll start with the translator add-on, and create a separate
module containing the code that performs the translation.

## Implementing "translate.js" ##

In the /lib directory under your translator's root, create a new file called
"translate.js" with the following contents:

    // Import the APIs we need.
    var request = require("request");

    // Define the 'translate' function using Request
    function translate(text, callback) {
      var req = request.Request({
          url: "http://ajax.googleapis.com/ajax/services/language/translate",
          content: {
            v: "1.0",
            q: text,
            langpair: "|en"
          },
          onComplete: function (response) {
            callback(response.json.responseData.translatedText);
          }
      });
      req.get();
    }

    // Export the 'translate' function
    exports.translate = translate;


The `translate` function here is essentially the same as the listener function
assigned to `onMessage` in the original code, except that it calls a callback
with the translation instead of assigning the result directly to the selection.

We export the function by assigning it to the global `exports` object.

## Editing "main.js" ##

Next we edit "main.js" to make it use our new module rather than the `request`
module:

    // Import the APIs we need.
    var contextMenu = require("context-menu");
    var selection = require("selection");
    var translator = require("translator");

    // Create a new context menu item.
    var menuItem = contextMenu.Item({
      label: "Translate Selection",
      // Show this item when a selection exists.
      context: contextMenu.SelectionContext(),
      // When this item is clicked, post a message to the item with the
      // selected text and current URL.
      contentScript: 'on("click", function () {' +
                     '  var text = window.getSelection().toString();' +
                     '  postMessage(text);' +
                     '});',

      // When we receive the message, call the translator with the
      // selected text and replace it with the translation.
      onMessage: function (text) {
        translator.translate(text, function(translation) {
                                      selection.text = translation; })
      }
    });

Next, execute `cfx run` again, and try it out. It should work in exactly the
same way as the previous version, except that now the core translator function
has been made available to other parts of your add-on or to *any other program*
that imports it.

## Testing Your Module ##

<span class="aside">
Note that for historical reasons the SDK also accepts unit tests which are
stored under "tests". In fact, right now only "tests" works for integration 
with cfx, but this will be fixed soon (see bug 
[614712](https://bugzilla.mozilla.org/show_bug.cgi?id=614712))
</span>
The SDK provides a framework to help test any modules you develop. According to
the 
[CommonJS package specification](http://wiki.commonjs.org/wiki/Packages/1.0)
unit tests should be kept in a directory called "test" under the package root.

If you follow this rule you can run tests using `cfx`. To demonstrate this we
will add some slightly unlikely tests for the translator module.

Create a new directory under the package root called "tests", and in it create
a file called "test-translator.js" with the following contents:

    var translator = require("translator")
    var testRunner;
    var remainingTests;

    function check_translation(translation) {
      testRunner.assertEqual("Lizard", translation);
      testRunner.done();
    }

    function test_languages(test, text) {
      testRunner= test;
      testRunner.waitUntilDone(2000);
      translator.translate(text, check_translation);
    }

    exports.test_german = function(test) {
      test_languages(test, "Eidechse");
    }

    exports.test_italian = function(test) {
      test_languages(test, "Lucertola");
    }

    exports.test_finnish = function(test) {
      test_languages(test, "Lisko");
    }

This file exports three function, each of which expects to receive
a single argument which is an instance of [`test`](#module/api-utils/unit-test).

<span class="aside">
`waitUntilDone()` and `done()` are needed here because the translator is
asynchronous. To test an asynchronous function (a function that completes
using a callback, rather than a return value), you call `test.waitUntilDone(),`
supplying a delay time in milliseconds long enough for the function to
complete. You put the test assertion in the callback, then call `test.done()`
to signal that the test can finish.
</span>

`test_languages` calls `translate` and in the callback uses `test` to check that
the translation is as expected.

Now execute `cfx --verbose test` from under the package root directory.
You should see something like this:

    Running tests on Firefox 4.0b7/Gecko 2.0b7 ...
    info: executing 'test-translator.test_languages'
    info: pass: a == b == "Lizard"
    info: pass: a == b == "Lizard"
    info: pass: a == b == "Lizard"

    3 of 3 tests passed.
    OK

What happens here is that `cfx test` looks in the `tests` directory of your
package, loads any modules that start with the word `test`, and calls all
their exported functions, passing them a `test` object implementation as
their only argument.

Obviously, you don't have to pass the `--verbose` option to `cfx` if you don't
want to; doing so just makes the output easier to read.

## Next: Programming With the SDK ##

Next we'll take a look at some of the programming with the SDK modules,
starting with its [event handling framework](#guide/events).

  [CommonJS Specification]: http://wiki.commonjs.org/wiki/Modules/1.0
  [Globals]: #guide/globals
  [unit-test]: #module/api-utils/unit-test
