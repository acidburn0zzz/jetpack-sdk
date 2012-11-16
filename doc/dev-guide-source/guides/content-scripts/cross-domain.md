<!-- This Source Code Form is subject to the terms of the Mozilla Public
   - License, v. 2.0. If a copy of the MPL was not distributed with this
   - file, You can obtain one at http://mozilla.org/MPL/2.0/. -->

# Cross-domain Content Scripts #

By default, content scripts don't have any cross-domain privileges.
In particular:

* they are not able to access content hosted in an
[`iframe`](https://developer.mozilla.org/en-US/docs/HTML/Element/iframe), if that
content is served from a different domain
* they're not able to make cross-domain
[XMLHttpRequests](https://developer.mozilla.org/en-US/docs/DOM/XMLHttpRequest)