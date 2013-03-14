<!-- This Source Code Form is subject to the terms of the Mozilla Public
   - License, v. 2.0. If a copy of the MPL was not distributed with this
   - file, You can obtain one at http://mozilla.org/MPL/2.0/. -->

# Low-Level APIs #

Modules in this section implement low-level APIs. These
modules fall roughly into three categories:

* fundamental utilities such as
[collection](modules/sdk/util/collection.html) and
[url](modules/sdk/url.html). Many add-ons are likely to
want to use modules from this category.

* building blocks for higher level modules, such as
[events](modules/sdk/event/core.html),
[worker](modules/sdk/content/worker.html), and
[api-utils](modules/sdk/deprecated/api-utils.html). You're more
likely to use these if you are building your own modules that
implement new APIs, thus extending the SDK itself.

* privileged modules that expose powerful low-level capabilities
such as [window/utils](modules/sdk/window/utils.html) and
[xhr](modules/sdk/net/xhr.html). You can use these
modules in your add-on if you need to, but should be aware that
the cost of privileged access is the need to take more elaborate
security precautions. In many cases these modules have simpler,
more restricted analogs among the "High-Level APIs" (for
example, [windows](modules/sdk/windows.html) or
[request](modules/sdk/request.html)).

Most of these modules are not yet
["stable"](dev-guide/guides/stability.html). This means that there
is a higher chance that we will have to make incompatible changes to
them in future releases.

In the list below, the icons indicate whether the module is compatible
with Firefox for Android, Firefox Desktop, or both.

<ul id="module-index"></ul>
