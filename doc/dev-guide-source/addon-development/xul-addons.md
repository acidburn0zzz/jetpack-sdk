
# Using the SDK with XUL Add-ons #

With the Add-on SDK you can use SDK modules in a regular XUL-based add-on.
This can be helpful if you:

* want to use some of the SDK's APIs
* like the way modules help separate your code into testable and
reusable pieces
* want to gradually migrate an existing add-on over to the SDK.

**Note: this feature is experimental and may change or stop working in a
future SDK release.**

## Initializing the Add-on ##

Creating a XUL-based add-on with the SDK is very similar to creating an
SDK-based add-on. We assume you have already completed the
[Getting Started](dev-guide/addon-development/getting-started.html) tutorial
and will only focus on the steps specific to XUL add-ons here.

To get started, [run activate](dev-guide/addon-development/installation.html),
create an empty directory, navigate to it, and run:
<pre>
  cfx init --template xul
</pre>

This creates all the same files and directories as the regular `cfx init`,
with a few additions:

* it creates a new directory called `extension`: this is where you'll keep all
the files and directories implementing the XUL add-on. It also creates some
files and directories inside `extension` to enable `cfx` to work with the
add-on.
* it adds a `templatedir` field to your add-on's `package.json` file, pointing
it at the new `extension` directory: this tells `cfx` to use the
`extension` directory as the template for your add-on

## Adding XUL Files ##

All the files from your XUL extension - XUL specification, locale, skins, and
so on - should be placed in the `extension` directory.

This directory already contains `chrome.manifest` and `install.rdf`
files. You should edit the `chrome.manifest` to point to the relevant pieces
of your add-on, but note that this file already contains the instructions
[required to register `harness.js` in Firefox 4] [mdc-xpcom-registration].
Be careful not to overwrite the three instructions (`component`, `contract`,
and `category`) when adding your own stuff to chrome.manifest.

The `extension/install.rdf` file is the add-on's
[install manifest] [mdc-install]. It will be updated with
[information from package.json] [package-spec] when you run `cfx xpi`, but
for attributes that can't be specified in package.json, you'll have to edit
the manifest directly.

Once you've done that, you can run, test, and package your add-on using
the same `cfx` commands you would for a regular SDK-based add-on:

<pre>
  cfx test
  cfx run
  cfx xpi
</pre>

You can create your own modules, unit tests, and use the modules provided by
the SDK in a XUL add-on, just like you can do in a regular SDK-based add-on.
The only two differences are:

 * you must restart Firefox to install (uninstall, disable,
   upgrade and so on) a XUL-based add-on.
 * XUL-based add-ons can use the functionality unavailable to bootstrapped
   (restartless) add-ons, like using [chrome.manifest](https://developer.mozilla.org/en/Chrome_Registration)
   to register overlays and to define user interface in XUL.

For a complete list of the files `cfx init --template xul` creates under
extension, see <a href="dev-guide/addon-development/xul-addons.html#pregenerated_files">the following section</a>.

## Loading SDK Modules From Your Add-on ##

To load modules we'll need to get the harness XPCOM service provided by the SDK.
This service has the following contract ID:

<pre>@mozilla.org/harness-service;1?id=&lt;package id></pre>

where *&lt;package-id>* is your add-on's [Program ID](dev-guide/addon-development/program-id.html),
which can be found as the `id` key in your add-on's
`package.json` file:

    {
      "id": "jid0-i6WjYzrJ0UFR0pPPM7Znl3BvYbk",
      // other properties here
    }

To call the SDK modules from regular add-on code use code like this,
substituting your add-on's Program ID for the ID supplied here:

    function myAddon_loadSDKModule(module) {
      return Components.classes[
        "@mozilla.org/harness-service;1?id=jid0-i6WjYzrJ0UFR0pPPM7Znl3BvYbk"].
        getService().wrappedJSObject.loader.require(module);
    }
    myAddon_loadSDKModule("tabs").open("http://www.mozilla.org");
<br>

## <a name="pregenerated_files">Extra Files</a> ##

The add-on created by `cfx init --template xul` has a few additional files
and keys not present in a regular SDK add-on. This section explains their
purpose:

<table>
<colgroup>
<col width="35%">
<col width="65%">
</colgroup>

<tr>
  <td>
    <code>extension/components/harness.js</code>
  </td>
  <td>
  <p>The heart of any SDK-based add-on. It
  handles the startup and shutdown process of the module-based part of the
  add-on.</p>
  <p>Note that this file is copied from the SDK
  (<code>python-lib/cuddlefish/app-extension/components/harness.js</code>) to your
  add-on, so you may need to update it manually when upgrading the SDK.</p>
  </td>
</tr>

<tr>
  <td>
    <code>extension/chrome.manifest</code>
  </td>
  <td>
  <p>Contains the instructions
    <a href="https://developer.mozilla.org/en/XPCOM/XPCOM_changes_in_Gecko_2.0#Component_registration">
    required to register <code>harness.js</code> in Firefox 4</a>.</p>
  <p>Be careful not to overwrite the three instructions (<code>component</code>, <code>contract</code>,
    and <code>category</code>) when adding your own stuff to chrome.manifest.</p>
  </td>
</tr>

<tr>
  <td>
    <code>extension/install.rdf</code>
  </td>
  <td>
    <p>The add-on's
      <a href="https://developer.mozilla.org/en/Install_manifests">install manifest</a>.</p>
    <p>It will be updated with
      <a href="dev-guide/addon-development/package-spec.html">information from <code>package.json</code></a>
      when you run <code>cfx xpi</code>, but for attributes that can't be
      specified in <code>package.json</code>, you'll have to edit the manifest
      directly.</p>
  </td>
</tr>

<tr>
  <td>
    <code>extension/modules/module.jsm</code>
  </td>
  <td>
    <p>This is an example of using functionality available only to XUL add-ons
      and is used only in <code>tests/test-module.js</code>.</p>
    <p>You can safely remove both files, along with the reference to it in
     the <code>chrome.manifest</code>.</p>
  </td>
</tr>

<tr>
  <td>
    <code>package.json</code>
  </td>
  <td>
    <p>While this file exists for all SDK-based add-ons, it has two attributes
      specific to XUL-based add-ons:</p>
    <ul>
      <li><p><code>templatedir</code> lets <code>cfx</code> know about the
            <code>extension</code> directory with your
            XUL files.</p></li>
      <li><p><code>harnessClassID</code> matches the classID of the harness
            component specified in <code>chrome.manifest</code>. It's passed
            on to the <code>harness.js</code> component by <code>cfx</code>,
            so that the generic code in <code>harness.js</code> knows what classID it's
            supposed to respond to.</p></li>
      </ul>
  </td>
</tr>

</table>

  [mdc-xpcom-registration]: https://developer.mozilla.org/en/XPCOM/XPCOM_changes_in_Gecko_2.0#Component_registration
  [mdc-install]: https://developer.mozilla.org/en/Install_manifests
  [package-spec]: dev-guide/addon-development/package-spec.html

## Example ##

In this example we'll take a very simple XUL-based add-on and enable it to
use the SDK. The XUL-based add-on has the following directory structure:

<pre>
helloworld/
           chrome.manifest
           install.rdf
           chrome/
                  content/
                          browserOverlay.js
                          browserOverlay.xul

</pre>

`browserOverlay.xul` looks like this:

<script type="syntaxhighlighter" class="brush: xml"><![CDATA[

<?xml version="1.0"?>

<?xml-stylesheet type="text/css" href="chrome://global/skin/" ?>


<!DOCTYPE overlay SYSTEM
  "chrome://helloworld/locale/browserOverlay.dtd">

<overlay id="helloworld-browser-overlay"
  xmlns="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul">

  &nbsp;&nbsp;<script type="application/x-javascript"
    src="chrome://helloworld/content/browserOverlay.js" />

  &nbsp;&nbsp;<menupopup id="menu_ToolsPopup">
      <menuitem id="helloworld-hello-menu-item"
        label="Say Hello"
        oncommand="HelloWorld.BrowserOverlay.sayHello(event);" />
  </menupopup>

</overlay>

]]>
</script>

It just adds an item to the "Tools" menu labeled "Say Hello".

`browserOverlay.js` looks like this:

    if ("undefined" == typeof(HelloWorld)) {
      var HelloWorld = {};
    };

    HelloWorld.BrowserOverlay = {
      sayHello : function(aEvent) {
        window.alert("Hello World");
      }
    };


When the user selects the menu item the add-on displays an alert message.
We'll change it to use the SDK's [notifications](packages/addon-kit/docs/notifications.html) module instead.

### Initializing the Add-on ###

So to begin with we'll create a new directory, change into it, and run:

<pre>
mkdir helloworld
cd helloworld
cfx init --template xul
</pre>

### Adding the XUL Files ###

Copy the contents of your `chrome` directory into `extension`, to get a
directory structure like this:

<pre>
helloworld/extension/
                     chrome.manifest
                     install.rdf
                     chrome/
                            content/
                                    browserOverlay.js
                                    browserOverlay.xul
                     components
                     modules
</pre>

Edit `chrome.manifest` to add pointers to the overlay, leaving the original
contents alone:

<pre>
# This registers the 'harness' component, which is the entry point
# for the Addon SDK-based part of the extension.
component {0f5aba2e-2a33-4d8c-ba7c-4943dec63798} components/harness.js
contract @mozilla.org/harness-service;1?id=jid1-dBAel4XqQ66N8A {0f5aba2e-2a33-4d8c-ba7c-4943dec63798}
category profile-after-change test-harness @mozilla.org/harness-service;1?id=jid1-dBAel4XqQ66N8A

# This is used in tests/test-module.js to test that chrome.manifest
# was loaded for this extension.
resource test-res modules/

content helloworld                            chrome/content/
overlay chrome://browser/content/browser.xul  chrome://helloworld/content/browserOverlay.xul
</pre>

Now you can run, test, and package this add-on just like a normal SDK-based add-on:

<pre>
cfx run
</pre>

### Loading SDK modules ###

Finally, look up the value of your add-on's
[Program ID](dev-guide/addon-development/program-id.html),
and change `sayHello()` to load and use the `notifications` module:

    if ("undefined" == typeof(HelloWorld)) {
      var HelloWorld = {};
    };

    HelloWorld.BrowserOverlay = {
      sayHello : function(aEvent) {
        function myAddon_loadSDKModule(module) {
          return Components.classes[
            "@mozilla.org/harness-service;1?id=jid1-dBAel4XqQ66N8A"].
            getService().wrappedJSObject.loader.require(module);
        }
        myAddon_loadSDKModule("notifications").notify({text: "Hello world!"});
      }
    };
