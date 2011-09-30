
# XUL Migration Guide #

This guide aims to help you migrate a traditional XUL-based add-on
to the SDK.

First, we'll look at the benefits and limitations of
using the SDK, to help decide whether your add-on is a good candidate
for porting.

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
<td><p>Although we can't promise we'll never break a <a href="packages/addon-kit/addon-kit.html">supported API</a>, maintaining compatibility across Firefox versions is a top priority for us.</p>
<p>We've designed the APIs to be forward-compatible with the new <a href="https://wiki.mozilla.org/Electrolysis/Firefox">multiple process architecture</a> (codenamed Electrolysis) planned for Firefox.</p>
<p>We also expect to support both desktop and mobile Firefox using a single edition of the SDK: so you'll be able to write one extension and have it work on both products.</p></td>
</tr>

<tr>
<td> <strong><a name="security">Security</a></strong></td>
<td><p>If they're not carefully designed, Firefox add-ons can open the browser to attack by malicious web pages. Although it's possible to write insecure add-ons using the SDK, it's not as easy, and the damage that a compromised add-on can do is usually more limited.</p></td>
</tr>

<tr>
<td> <strong><a name="restartlessness">Restartlessness</a></strong></td>
<td><p>Add-ons built with the SDK are can be installed without having to restart Firefox.</p>
<p>Although you can write <a href="https://developer.mozilla.org/en/Extensions/Bootstrapped_extensions">traditional add-ons that are restartless</a>, you can't use XUL overlays in them, so most traditional add-ons would have to be substantially rewritten anyway.</p></td>
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
<a href="https://developer.mozilla.org/en/Extensions/Bootstrapped_extensions">bootstrapped extension</a>

Alternatively, you can load third-party modules, which extend the SDK's
core APIs.

In this guide we'll look at all these techniques, but note that by
doing this you lose some of the benefits of programming with the SDK
including simplicity, compatibility, and to a lesser extent security.

Note, though, that all SDK-based add-ons are restartless, so you can't
use XUL overlays in SDK-based add-ons.

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

In a XUL-based add-on, code that uses XPCOM objects and manipulates the
browser chrome runs in the same context as code that interacts with web
pages. But the SDK makes a distinction between:

* add-on scripts, which can use the SDK APIs, but is not able to interact with 
web pages

* content scripts, which can access web pages, but do not have access to the
SDK's APIs

Content scripts and add-on scripts communicate by sending each other JSON
messages: in fact, the ability to communicate with the add-on scripts is the
only extra privilege a content script is granted over a normal remote web
page script.

