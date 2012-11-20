<!-- This Source Code Form is subject to the terms of the Mozilla Public
   - License, v. 2.0. If a copy of the MPL was not distributed with this
   - file, You can obtain one at http://mozilla.org/MPL/2.0/. -->

# Cross-domain Content Scripts #

By default, content scripts don't have any cross-domain privileges.
In particular, they can't:

* [access content hosted in an `iframe`, if that content is served from a different domain](dev-guide/guides/content-scripts/cross-domain.html#Cross-domain iframes)
* [make cross-domain XMLHttpRequests](dev-guide/guides/content-scripts/cross-domain.html#Cross-domain XMLHttpRequest)

However, you can enable these features for specific domains
by adding them to your add-on's [package.json](dev-guide/package-spec.html)
under the `"content-permissions"` key:

<pre>
"content-permissions": ["http://example.org/", "http://example.com/"]
</pre>

* The domains listed must include the scheme and fully qualified domain name,
and these must exactly match the domains serving the content - so in the
example above, the content script will not be allowed to access content
served from `https://example.com/`.
* Wildcards are not allowed.
* This feature is currently only available for content scripts, not for page
scripts included in HTML files shipped with your add-on.

## Cross-domain iframes ##

The following "main.js" creates a page-worker which loads a local HTML file
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

For this to work, we need to add the `"content-permissions"` key to
"package.json":

<pre>
"content-permissions": ["http://en.m.wikipedia.org/"]
</pre>

The add-on should successfully retrieve the iframe's content.

## Cross-domain XMLHttpRequest ##

The following add-on creates a panel whose content is the latest
tweet from the [@mozhacks Twitter account](https://twitter.com/mozhacks).

The "main.js":

* creates a panel whose content is supplied by "panel.html" and
adds a content script "panel-script.js" to it
* sends the panel a "show" message when it is shown
* attaches the panel to a widget

<!-- terminate Markdown list -->

    // main.js
    var data = require("self").data;

    var tweet_panel = require("panel").Panel({
      height: 50,
      contentURL: data.url("panel.html"),
      contentScriptFile: data.url("panel-script.js")
    });

    tweet_panel.on("show", function(){
      tweet_panel.port.emit("show");
    });

    require("widget").Widget({
      id: "mozhacks_tweets",
      label: "@mozhacks tweets",
      contentURL: "https://hacks.mozilla.org/favicon.ico",
      panel: tweet_panel
    });

The "panel.html" just includes a `<div>` block for the tweet:

<pre class="brush: html">
&lt;!doctype HTML&gt;
&lt;!-- panel.html --&gt;

&lt;html&gt;
  &lt;head&gt;&lt;/head&gt;
  &lt;body&gt;
    &lt;div id="mozhacks_tweet">&lt;/div&gt;
  &lt;/body&gt;
&lt;/html&gt;
</pre>

The "panel-script.js" uses [XMLHttpRequest](https://developer.mozilla.org/en-US/docs/DOM/XMLHttpRequest)
to fetch the latest tweet:

    // panel-script.js
    var url = "https://api.twitter.com/1/statuses/user_timeline.json?screen_name=mozhacks&count=1";

    self.port.on("show", function () {
      var request = new XMLHttpRequest();
      request.open("GET", url, true);
      request.onload = function () {
        var jsonResponse = JSON.parse(request.responseText);
        var element = document.getElementById("mozhacks_tweet");
        element.textContent = jsonResponse[0].text;
      };
      request.send();
    });

Finally, we need to add the `"content-permissions"` key to "package.json":

<pre>
"content-permissions": ["https://api.twitter.com"]
</pre>

## Content Permissions and unsafeWindow ##

If you use `"content-permissions"`, then JavaScript values in content
scripts will not be available from pages. Suppose your content script includes
a line like:

    // content-script.js:
    unsafeWindow.myCustomAPI = function () {};

If you have included the `"content-permissions"` key, when the page script
tries to access `myCustomAPI` this will result in a "permission denied"
exception.
