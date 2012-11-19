<!-- This Source Code Form is subject to the terms of the Mozilla Public
   - License, v. 2.0. If a copy of the MPL was not distributed with this
   - file, You can obtain one at http://mozilla.org/MPL/2.0/. -->

# Cross-domain Content Scripts #

By default, content scripts don't have any cross-domain privileges.
In particular:

* [they can't access content hosted in an `iframe`, if that content is served from a different domain](dev-guide/guides/content-scripts/cross-domain.html#Cross-domain iframes)
* [they can't make cross-domain XMLHttpRequests](dev-guide/guides/content-scripts/cross-domain.html#Cross-domain XMLHttpRequest)

However, you can enable these features for specific domains
by adding them to your add-on's [package.json](dev-guide/package-spec.html)
under the `"content-permissions"` key:

<pre>
"content-permissions": ["http://example.org/", "http://example.com/"]
</pre>

The domains listed must include the scheme and fully qualified domain name,
and these must exactly match the domains serving the content - so in the
example above, the content script will not be allowed to access content
served from `https://example.com/`. Wildcards are not allowed.

If you use `"content-permissions"`, then JavaScript values in content
scripts will not be available from pages. Suppose your content script includes
a line like:

    // content-script.js:
    unsafeWindow.myCustomAPI = function () {};

If the page script tries to access `myCustomAPI`, this will result in
a "permission denied" exception.

## Cross-domain iframes ##

The following add-on creates a page-worker which loads a local HTML file
called "page.html", attaches a content script called "page.js" to the
page, waits for messages from the script, and logs the payload.

    //main.js
    var data = require("self").data;

    var pageWorker = require("page-worker").Page({
      contentURL: data.url("page.html"),
      contentScriptFile: data.url("page-script.js")
    });

    pageWorker.on("message", function(message) {
      console.log(message);
    });

The "page.html" file embeds an iframe whose content is
served from "http://en.m.wikipedia.org/":

<pre class="brush: html">
    &lt;!doctype html&gt;
    &lt;!-- page.html --&gt;
    &lt;html&gt;
      &lt;head>&lt;/head&gt;
      &lt;body&gt;
        &lt;iframe id="wikipedia" src="http://en.m.wikipedia.org/"&gt;&lt;/iframe&gt;
      &lt;/body&gt;
    &lt;/html&gt;
</pre>

The "page-script.js" file just sends the iframe's content to "main.js":

    // page-script.js
    var iframe = window.document.getElementById("wikipedia");
    self.postMessage(iframe.contentWindow.document.body.innerHTML);

If we run this add-on we'll see an error like this:

<pre>
error: x-domain: An exception occurred.
Traceback (most recent call last):
  File "resource://jid1-bc7g8hwsqmemdq-at-jetpack/x-domain/data/page-script.js", line 4, in 
    self.postMessage(iframe.contentWindow.document.body.innerHTML);
Error: Permission denied to access property 'document'
</pre>

Now try adding this line to the add-on's "package.json" file:

<pre>
"content-permissions": ["http://en.m.wikipedia.org/"]
</pre>

The add-on should successfully retrieve the iframe's content.

## Cross-domain XMLHttpRequest ##

THe following add-on creates a panel whose content is 