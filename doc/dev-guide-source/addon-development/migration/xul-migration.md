
# XUL Migration Guide #

This guide aims to help you migrate a traditional XUL-based add-on
to the SDK.

First, we'll look at the [benefits and limitations of
using the SDK](/dev-guide/addon-development/migration/benefits_limitations.html),
to help decide whether your add-on is a good candidate for porting.

Next, we'll look at each of the three main tasks involved in migrating
to the SDK: working with content scripts, UI development without XUL overlays,
and working with XPCOM.

Finally, we'll walk through a simple example.

## Benefits and Limitations of the SDK ##

For developers already familiar with XUL and XPCOM development, the main
advantages of the SDK are:

<table>
<colgroup>
<col width="20%">
<col width="80%">
</colgroup>
<tr>
<td> <strong><a name="compatibility">Compatibility</a></strong></td>
<td><p>Although we can't promise we'll never break a
<a href="packages/addon-kit/addon-kit.html">supported API</a>,
maintaining compatibility across Firefox versions is a top priority for us.</p>
<p>We've designed the APIs to be forward-compatible with the new
<a href="https://wiki.mozilla.org/Electrolysis/Firefox">multiple process architecture</a>
(codenamed Electrolysis) planned for Firefox.</p>
<p>We also expect to support both desktop and mobile Firefox using a single
edition of the SDK: so you'll be able to write one extension and have it work
on both products.</p></td>
</tr>

<tr>
<td> <strong><a name="security">Security</a></strong></td>
<td><p>If they're not carefully designed, Firefox add-ons can open the browser
to attack by malicious web pages. Although it's possible to write insecure
add-ons using the SDK, it's not as easy, and the damage that a compromised
add-on can do is usually more limited.</p></td>
</tr>

<tr>
<td> <strong><a name="restartlessness">Restartlessness</a></strong></td>
<td><p>Add-ons built with the SDK are can be installed without having
to restart Firefox.</p>
<p>Although you can write
<a href="https://developer.mozilla.org/en/Extensions/Bootstrapped_extensions">
traditional add-ons that are restartless</a>, you can't use XUL overlays in
them, so most traditional add-ons would have to be substantially rewritten
anyway.</p></td>
</tr>

</table>

The main advantages XUL-based add-ons have are:

<table>
<colgroup>
<col width="20%">
<col width="80%">
</colgroup>
<tr>
<td><strong><a name="ui_flexibility">User interface flexibility</a></strong></td>
<td><p>XUL overlays offer a great deal of options for building a UI and
integrating it into the browser. Using only the SDK's supported APIs you have
much more limited options for your UI.</p></td>
</tr>

<tr>
<td><strong><a name="xpcom_access">XPCOM</a></strong></td>
<td><p>Traditional add-ons have access to a vast amount of Firefox
functionality via XPCOM. The SDK exposes a relatively small set of this
functionality.</p></td>
</tr>

<tr>
<td><strong><a name="localization">Localization Support</a></strong></td>
<td><p>The SDK doesn't yet support localization.</p></td>
</tr>

</table>

### Low-level APIs and Third-party Modules ###

That's not the whole story. If you need more flexibility than the SDK's
["supported" APIs](packages/addon-kit/addon-kit.html) provide, you can
use its ["low-level" APIs](packages/api-utils/api-utils.html) to load
XPCOM objects directly or to manipulate the DOM directly as in a
traditional
<a href="https://developer.mozilla.org/en/Extensions/Bootstrapped_extensions">bootstrapped extension</a>.

Alternatively, you can load third-party modules, which extend the SDK's
core APIs.

In this guide we'll look at all these techniques, but note that by
doing this you lose some of the benefits of programming with the SDK
including simplicity, compatibility, and to a lesser extent security.

### Should You Migrate? ###

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

## Content Scripts ###

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

A XUL-based add-on will need to be reorganized to respect this distinction.

This design is motivated by two related concerns. First is security: it
reduces the risk that a malicious web page will be able to access privileged
APIs. Second is the need to be compatible with the multi-process architecture
planned for Firefox and already partly implemented in Firefox Mobile. Note
that all mobile add-ons already need to use
[a similar design](https://wiki.mozilla.org/Mobile/Fennec/Extensions/Electrolysis).

There's much more information on content scripts in the
[Working With Content Scripts](dev-guide/addon-development/web-content.html) guide.

## UI Development Without XUL Overlays ##

Since you can use XUL overlays in SDK-based add-ons, you need to find
alternative ways to modify the browser chrome. There are three options:

* use the SDK's supported APIs
* use third-party modules
* use the SDK's low-level APIs to manipulate the XUL dynamically

### SDK APIs ###

The APIs the SDK provides for building user interfaces are summarized in the
table below.

<table>
<colgroup>
<col width="20%">
<col width="80%">
</colgroup>
<tr>
<td> <strong><a href="packages/addon-kit/docs/panel.html">panel</a></strong></td>
<td><p>A panel is the SDK's version of a dialog. Its content and appearance
is specified using HTML, CSS and JavaScript.

You can build or load the content locally or load it from a remote server.</p>
<img class="image-center" src="static-files/media/screenshots/modules/panel-tabs-osx.png"
alt="List open tabs panel">
<br>
</td>
</tr>

<tr>
<td> <strong><a href="packages/addon-kit/docs/widget.html">widget</a></strong></td>
<td><p>The widget is the SDK's replacement for toolbars and toolbar buttons.
Its content is specified using HTML, or as an icon. By specifying the content
as an icon you can create a toolbar button:</p>

<img class="image-center" src="static-files/media/screenshots/modules/widget-icon-osx.png"
alt="Mozilla widget icon">
<br>
<p>By specifying it as HTML you can create a toolbar, or any other kind of
compact user interface content:</p>
<img class="image-center" src="static-files/media/screenshots/modules/widget-content-osx.png"
alt="Mozilla widget content">
<br>

<p>Widgets always appear by default in the
<a href="https://developer.mozilla.org/en/The_add-on_bar">add-on bar</a>,
although users may relocate them by
<a href="http://support.mozilla.com/en-US/kb/how-do-i-customize-toolbars">toolbar customization</a>.

</p>

</td>
</tr>

<tr>
<td> <strong><a href="packages/addon-kit/docs/context-menu.html">context-menu</a></strong></td>
<td><p>The <code>context-menu</code> module lets you add items and submenus
to the browser's context menu.</p>

<img class="image-center" src="static-files/media/screenshots/modules/context-menu-image-osx.png"
alt="Context-menu">
<br>
<p>Note that there is currently no way to add items to the browser's main menus
using the SDK's supported APIs.</p>

</td>
</tr>

<tr>
<td> <strong><a href="packages/addon-kit/docs/notifications.html">notifications</a></strong></td>
<td>
<p>This module enables an add-on to display transient messages to the user.
On Mac OS X a notification will look something like this:</p>

<img class="image-center" src="static-files/media/screenshots/modules/notification-growl-osx.png"
alt="Growl notification">
<br>
</td>
</tr>

</table>

APIs like `widget` and `panel` are very generic, and with the right content
can be used to replace many particular XUL elements.

But there are some notable limitations in the SDK APIs, and even a fairly
simple UI may need some degree of redesign to work with them. In particular,
the default placement of widgets and the inability to add main menu items are
commonly encountered as obstacles in migrating to the SDK. These are
intentional design choices, the belief being that it makes for a better user
experience for add-ons to expose their interfaces in a consistent way. So
it's worth considering changing your user interface to align with the SDK
APIs.

Having said that, add-ons which make drastic changes to the appearance
of the browser chrome will certainly need more than the SDK's supported APIs
can offer.

### Third-party Modules ###

The SDK is extensible by design: it's possible for developers to use its
low-level APIs to expose 