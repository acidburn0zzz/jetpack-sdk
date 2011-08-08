# Why Migrate? #

This guide aims to explain the benefits and limitations of SDK-based add-ons compared to XUL-based add-ons, and help you decide whether migrating from XUL is the right choice for you.

The most obvious advantage of the Add-on SDK is that it provides a simpler environment for developing add-ons than the traditional approach. With the SDK you can write add-ons with standard Web tools like JavaScript, HTML and CSS, rather than having to learn the nonstandard XUL and XPCOM technologies. Also, the SDK provides tools which make is easy to package an add-on as an XPI file. For someone new to Firefox add-on development, these advantages might seem compelling.

But if you've already learned XUL and XPCOM, and been through the process of building an XPI file, why should you migrate to the SDK, and have to learn a whole new set of APIs and tools?

## The Summary ##

A simplistic way to explain this is to say that the SDK:

* offers APIs that will not change with new releases of Firefox
* makes it easier to secure add-ons
* creates "restartless" add-ons: add-ons which the user can install without restarting the browser
* makes for more consistent user interfaces

The cost of this is a loss of power and flexibility. XUL-based add-ons:

* have much more control over the user interface
* have full access to the power of XPCOM
* support localization

## The Reality ##

In reality, SDK-based add-ons:

* can be made to do most of the things that XUL-based add-ons can do
* can be just as insecure
* can use just as unstable APIs.

The SDK provides a set of ["supported" APIs](packages/addon-kit/addon-kit.html). If you stick to these APIs you get the benefits listed above, but also have to live with the constraints.

If you need to exceed the constraints you can use the ["low-level" APIs](packages/api-utils/api-utils.html) to build much more complex and sophisticated SDK-based add-ons, but in doing so you lose some of the benefits of programming with the SDK, including simplicity, compatibility and to a lesser extent security.

Note, though, that all SDK-based add-ons are restartless, and although it is possible to write traditional add-ons that are restartless, they can't use XUL overlays.

<img class="image-center" src="media/addon-dependencies.png"
alt="Add-on use of supported and low-level modules">
<br>

### Advantages of SDK-Based Add-ons ###

<table>
<colgroup>
<col width="30%">
<col width="70%">
</colgroup>
<tr>
<td> <strong><a name="compatibility">Compatibility</a></strong></td>
<td><p>Although we can't promise we'll never break a <a href="packages/addon-kit/addon-kit.html">supported API</a>, maintaining compatibility across Firefox versions is a top priority for us.</p>
<p>We've designed the APIs to be forward-compatible with the new <a href="https://wiki.mozilla.org/Electrolysis/Firefox">multiple process architecture</a> (codenamed Electrolysis) planned for Firefox.</p>
<p>We also expect to support both desktop and mobile Firefox using a single edition of the SDK: so you'll be able to write one extension and have it work on both products.</p></td>
</tr>

<tr>
<td> <strong><a name="security">Security</a></strong></td>
<td><p>If they're not carefully designed Firefox add-ons can open the browser to attack by malicious web pages. Although it's possible to write insecure add-ons using the SDK, it's not as easy, and the damage that a compromised add-on can do is more limited.</p>
<p>There are two main reasons for this. 
  <ul>
    <li>First, SDK-based modules don't run with full browser privileges: they can only use the APIs they explicitly import. Of course, modules that <a href="dev-guide/module-development/chrome.html"><code>require("chrome")</code></a> run with full privileges.</li><br>
    <li>Second, code that interacts with web pages doesn't have direct access to the SDK APIs at all, and is only able to communicate with the rest of the add-on via a message-passing API.</li>
  </ul>
</p></td>
</tr>

<tr>
<td> <strong><a name="restartlessness">Restartlessness</a></strong></td>
<td><p>Add-ons built with the SDK are can be installed without having to restart Firefox.</p>
<p>Although you can write <a href="https://developer.mozilla.org/en/Extensions/Bootstrapped_extensions">traditional add-ons that are restartless</a>, you can't use XUL overlays in them, so most traditional add-ons would have to be substantially rewritten anyway.</p></td>
</tr>

<tr>
<td> <strong><a name="consistent_ux">Consistent User Experience</a></strong></td>
<td><p>XUL-based add-ons allow for complete flexibility in your UI design. One consequence of this is that it's easy for add-ons to provide a confusing and inconsistent user experience, especially when different add-ons expose their interfaces in very different ways.</p>
<p>User interfaces built with the SDK are integrated consistently into the browser, and the user will find it easier to access their functionality. The flip side of this, of course, is that the SDK's APIs may not be suitable for add-ons which need complex UIs.</p></td>
</tr>

</table>

### Advantages of XUL-Based Add-ons ###

<table>
<colgroup>
<col width="30%">
<col width="70%">
</colgroup>
<tr>
<td><strong><a name="ui_flexibility">User interface flexibility</a></strong></td>
<td><p>XUL overlays offer a great deal of options for building a UI and integrating it into the browser. Using only the SDK's supported APIs you have much more limited options for your UI.</p>
<p>If the supported APIs doesn't provide the UI you need, you can manipulate the DOM directly as in a traditional <a href="https://developer.mozilla.org/en/Extensions/Bootstrapped_extensions">bootstrapped extension</a>. We'll discuss how to do this, but it's complex, and gives up the compatibility benefit of using the SDK.</p></td>
</tr>

<tr>
<td><strong><a name="xpcom_access">XPCOM</a></strong></td>
<td>Traditional add-ons have access to a vast amount of Firefox functionality via XPCOM. The SDK exposes a relatively small set of this functionality. Again, you can use XPCOM directly in the context of an SDK-based extension, but stand to lose some of the benefits, in particular compatibility and security.</td>
</tr>

<tr>
<td><strong><a name="localization">Localization Support</a></strong></td>
<td>The SDK doesn't yet support localization.</td>
</tr>

</table>

## Should You Migrate? ##

Whether you should migrate a particular add-on is largely a matter of how well the SDK's supported APIs meet its needs.

* If your add-on can accomplish everything it needs using only the supported APIs, it's a good candidate for migration.

* If your add-on needs a lot of help from the low-level APIs, then you won't see much benefit from migrating.

* If your needs a fairly limited amount of help from low-level APIs, then it might still be worth migrating: we'll add more supported APIs in future releases to meet important use cases, and eventually hope to have a comprehensive collection of third party modules filling many of the gaps.
