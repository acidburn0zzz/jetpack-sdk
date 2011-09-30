
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

## [Benefits and Limitations of the SDK](dev-guide/addon-development/migration/why-migrate.html) ##

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

That's not 