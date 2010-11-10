This section of the tutorial takes you through the process of implementing,
running and packaging a simple add-on using the SDK. The add-on will add a
menu item to Firefox's context menu that replaces selected text with its
English translation.

First, create a directory under the SDK root called "translator". This is
where we will keep all the files for this add-on.

## Packages, modules, and add-ons ##
Before we start it's worth taking s short detour into CommonJS, as this is the
underlying infrastructure for both modules and add-ons.

The [CommonJS group](http://wiki.commonjs.org/wiki/CommonJS) defines
specifications for ***modules*** and ***packages***. 

A CommonJS **module** is a piece of reusable JavaScript: it exports certain
objects which are thus made available to dependent code. To facilitate this
CommonJS defines:

* an object called `exports` which contains all the objects which a CommonJS
module wants to make available to other modules
* a function called `require` which a module can use to import the exports 
object of another module

A CommonJS **package** is a structure which can wrap a collection of related
modules: this makes it easier to distribute, install and manage modules.
Minimally, a package must include a package specification file named
"package.json". Among other things this file describes the other CommonJS
packages that this package depends on. Packages must also follow a particular
directory structure.

* The JavaScript modules which the SDK provides are CommonJS modules, and they
are collected into CommonJS packages.

* The JavaScript components of an add-on constitute one or more
CommonJS modules, and a complete add-on is a CommonJS package.

So in terms of CommonJS objects we could depict the translator add-on as
follows:

![CommonJS translator](media/commonjs-translator.jpg)

## Package specification ##
Since an add-on is a CommonJS package, the first file we will create is the
package specification file.

In your "translator" directory create a file called "package.json" and give it
the following contents:

    {
      "description": "Translates selected text into English.",
      "author": "Me (http://me.org)",
      "dependencies": ["addon-kit"]
    }

The "dependencies" line asserts that this add-on will be using modules from
the addon-kit package. 

## Adding Your Code ##
According to the CommonJS package definition, all JavaScript modules are kept
in a directory named "lib" under the top level directory.

If a module called "main" exists in a CommonJS package, that module will be
evaluated as soon as your program is loaded. For an add-on, that means that
the "main" module will be evaluated as soon as the host application, such as
Firefox or Thunderbird has enabled your program as an extension.

So: we create a directory called "lib" under the root "translator" directory,
and in that directory add a file called "main.js" with the following content:

    // Import the APIs we need.
    var contextMenu = require("context-menu");
    var request = require("request");
    var selection = require("selection");

    // Create a new context menu item.
    var menuItem = contextMenu.Item({

      label: "Translate Selection",

      // Show this item when a selection exists.
      context: contextMenu.SelectionContext(),

      // When this item is clicked, post a message to the item with the
      // selected text and current URL.
      contentScript: 'on("click", function () {' +
                     '  var text = window.getSelection().toString();' +
                     '  postMessage({ text: text, url: document.URL });' +
                     '});',

      // When we receive the message, call the Google Translate API with the
      // selected text and replace it with the translation.
      onMessage: function (selectionInfo) {
        var req = request.Request({
          url: "http://ajax.googleapis.com/ajax/services/language/translate",
          content: {
            v: "1.0",
            q: selectionInfo.text,
            langpair: "|en"
          },
          headers: {
            Referer: selectionInfo.url
          },
          onComplete: function (response) {
            selection.text = response.json.responseData.translatedText;
          }
        });
        req.get();
      }
    });

    // Add the new menu item to the application's context menu.
    contextMenu.add(menuItem);

The first three lines are used to import three SDK modules from the
addon-kit package:

* **`context-menu`** enables add-ons to add new items to the context menu
* **`request`** enables add-ons to make network requests
* **`selection`** gives add-ons access to selected text in the active browser
window

Next, this code constructs a context menu item. It supplies:

* the name of the item to display
* a context in which the item should be displayed (in this case, whenever some
text on the page is selected)
* a script to execute when the item is clicked: this script sends the selected
text and document URL to the function assigned to the onMessage parameter
* a value for the onMessage parameter: this function will now be called with
the selected text and document URL, whenever the user clicks the menu. It uses
Google's AJAX-based translation service to translate the selection to English
and sets the selection to the translated text.

Finally the code adds the new menu item to the context menu.

## Running It ##
To run your program, navigate to the root of your package directory
in your shell and run:

    cfx run

The first time you do this, you'll see a message like this:

    No 'id' in package.json: creating a new keypair for you.
    package.json modified: please re-run 'cfx run'
 
Run it again, and it will run an instance of Firefox (or your default
application) with your add-on installed.

## Packaging It ##
To install an add-on it must be packaged as an
[XPI file](https://developer.mozilla.org/en/XPI). The SDK
simplifies the packaging process by generating this file for you.

To package your program as a XPI, navigate to the root of your package
directory in your shell and run `cfx xpi`. You should see a message like this:

    Exporting extension to translator.xpi.

The `translator.xpi` file can be found in the directory in which you ran the
command.

###The Program ID###
The ID that `cfx` generated the first time you executed `cfx run` is called the
**Program ID** and it is important. It is a unique identifier for your add-on
and is used for a variety of purposes. For example: mozilla.addons.org uses it
to distinguish between new add-ons and updates to existing add-ons, and the
[simple-storage](#module/addon-kit/simple-storage) module uses it to figure out
which stored data belongs to which add-on.

<span class="aside">
where is it on Windows?
</span>

The program ID is actually the public part of a cryptographic key pair. When
cfx generates a program ID it actually generates a pair of related keys: one
half (the public key) is embedded in package.json as the program ID while the
other half (the private key) gets stored in a file in ~/.jetpack/keys.

When the XPI file is generated it is signed with the private key. Then the
browser, or some other tool, can use the public key to verify that the XPI file
was actually signed by the author.

The private key is very important! If you lose it, you will not be able to
upgrade your add-on: you'll have to create a new add-on ID, and your users will
have to manually uninstall the old one and install the new one. If somebody
else gets a copy of your private key, they will be able to write add-ons that
could impersonate and displace your own.

The add-on's private key needs to be available (in ~/.jetpack/keys/) on any
computer that you use to build that add-on. When you copy the add-on source
code to a new machine, you also need to copy the private key (`cfx xpi` will
remind you of this). The best idea is to just copy the whole ~/.jetpack
directory to a USB flash drive that you can carry with you. It is not stored
in your package source tree, so that you can show your code to somebody else
without also giving them the ability to create forged upgrades for your add-on.

If you start your add-on work by copying somebody else's source code, you'll
need to remove their Program ID from the package.json file before you can build
your own XPIs. Again, cfx xpi will remind you of this, and your options, when
you attempt to build an XPI from a package.json that references a private key
that you don't have in ~/.jetpack/keys/.

## Checking the Package ##
If you'd like to test the packaged program before distributing it,
you can run it from the shell with:

    mozrunner -a test.xpi

Or you can install it from the Firefox Add-ons Manager itself, as
you would when testing a traditional add-on.

## Distributing It ##
To distribute your program, you can upload it to
[Addons.mozilla.org](http://addons.mozilla.org).
Eventually, this step may be automated via the SDK, streamlining the
distribution process further.

## Next: Jetpack modules ##
The next section provides an [overview of the SDK 
modules](#guide/module-overview).

  [Packaging]: #guide/packaging
  [troubleshooting]: #guide/troubleshooting
