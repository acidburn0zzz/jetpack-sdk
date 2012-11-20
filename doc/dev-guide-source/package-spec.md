<!-- This Source Code Form is subject to the terms of the Mozilla Public
   - License, v. 2.0. If a copy of the MPL was not distributed with this
   - file, You can obtain one at http://mozilla.org/MPL/2.0/. -->

# package.json #

The "package.json" file contains metadata for your add-on.

Some of its entries, such as [`icon`](dev-guide/package-spec.html#icon),
[`name`](dev-guide/package-spec.html#name), and
[`description`](dev-guide/package-spec.html#description), have
direct analogues in the
[install manifest](https://developer.mozilla.org/en-US/docs/Install_Manifests)
format, and entries from package.json are written into the install
manifest when the add-on is built using [`cfx xpi`](dev-guide/cfx-tool.html#cfx xpi).

Others, such as
[`lib`](dev-guide/package-spec.html#lib),
[`content-permissions`](dev-guide/package-spec.html#content-permissions),
and [`preferences`](dev-guide/package-spec.html#preferences),
represent instructions to the cfx tool itself to generate and include
particular code and data structures in your add-on.

The `package.json` file is initially generated in your add-on's root
directory the first time you run
[`cfx init`](dev-guide/cfx-tool.html#cfx init):

<pre>
{
  "name": "my-addon",
  "fullName": "my-addon",
  "description": "a basic add-on",
  "author": "",
  "license": "MPL 2.0",
  "version": "0.1"
}
</pre>

`package.json` may contain the following keys:

<table>

<colgroup>
  <col width="20%"></col>
  <col width="80%"></col>
</colgroup>

<tr>
  <td id="name"><code>name</code></td>
  <td><p>The add-on's name. This name cannot contain spaces or periods, and
  defaults to the name of the parent directory.</p><p>When the add-on is
  built as an XPI, if the <a href="dev-guide/package-spec.html#fullName"><code>fullName</code></a>
  key is not present, <code>name</code> is used as the add-on's
  <a href="https://developer.mozilla.org/en-US/docs/Install_Manifests#name"><code>em:name</code></a>
  element in its "install.rdf".</p></td>
</tr>

<tr>
  <td id="fullName"><code>fullName</code></td>
  <td><p>The full name of the package. It can contain spaces.<p></p>
  If this key is present its value will be used as the add-on's
  <a href="https://developer.mozilla.org/en-US/docs/Install_Manifests#name"><code>em:name</code></a>
  element in its "install.rdf".</p></td>
</tr>

<tr>
  <td id="description"><code>description</code></td>
  <td><p>The add-on's description. This defaults to the text "a basic add-on".</p>
  <p>This value will be used as the add-on's
  <a href="https://developer.mozilla.org/en-US/docs/Install_Manifests#description"><code>em:description</code></a>
  element in its "install.rdf".</p></td>
</tr>

<tr>
  <td id="author"><code>author</code></td>
  <td><p>The original author of the package, initialized to an empty string.
  It may include a optional URL in parentheses and an email
  address in angle brackets.</p>
  <p>This value will be used as the add-on's
  <a href="https://developer.mozilla.org/en-US/docs/Install_Manifests#creator"><code>em:creator</code></a>
  element in its "install.rdf".</p></td>
</tr>

<tr>
  <td id="contributors"><code>contributors</code></td>
  <td><p>This may be an array of additional <a href="dev-guide/package-spec.html#author"><code>author</code></a>
  strings.</p>
  <p>These values will be used as the add-on's
  <a href="https://developer.mozilla.org/en-US/docs/Install_Manifests#contributor"><code>em:contributor</code></a>
  elements in its "install.rdf".</p></td>
</tr>

<tr>
  <td id="homepage"><code>homepage</code></td>
  <td><p>The URL of the package's website.</p>
  <p>This value will be used as the add-on's
  <a href="https://developer.mozilla.org/en-US/docs/Install_Manifests#homepageURL"><code>em:homepageURL</code></a>
  element in its "install.rdf".</p></td>
</tr>

<tr>
  <td id="icon"><code>icon</code></td>
  <td><p>the relative path from the root of the package to a
  PNG file containing the icon for the package. By default, this
  is `icon.png`. If the package is built as an XPI, this is used
  as the add-on's icon to display in the Add-on Manager's add-ons list.
  This key maps on to the
  [`iconURL` entry in the Install Manifest](https://developer.mozilla.org/en/install_manifests#iconURL),
  so the icon may be up to 48x48 pixels in size.</p></td>
</tr>

<tr>
  <td id="icon64"><code>icon64</code></td>
  <td><p>the relative path from the root of the package to a
  PNG file containing the icon64 for the package. By default, this
  is `icon64.png`. If the package is built as an XPI, this is used
  as the add-on's icon to display in the Addon Manager's add-on details view.
  This key maps on to the
  [`icon64URL` entry in the Install Manifest](https://developer.mozilla.org/en/install_manifests#icon64URL),
  so the icon should be 64x64 pixels in size.</p></td>
</tr>

<tr>
  <td id="preferences"><code>preferences</code></td>
  <td><p>An array of JSON objects that use the following keys `name`, `type`, `value`,
  `title`, and `description`.  These JSON objects will be used to automatically
  create a preferences interface for the addon in the Add-ons Manager.
  For more information see the documentation of [simple-prefs](modules/sdk/simple-prefs.html).
</p></td>
</tr>

<tr>
  <td id="license"><code>license</code></td>
  <td><p>the name of the license as a String, with an optional
  URL in parentheses.</p></td>
</tr>

<tr>
  <td id="id"><code>id</code></td>
  <td><p>a globally unique identifier for the package. When the package is
   built as an XPI, this is used as the add-on's `em:id` element in its
  `install.rdf`. See the
  [Program ID page](dev-guide/guides/program-id.html).</p></td>
</tr>

<tr>
  <td id="version"><code>version</code></td>
  <td><p>a String representing the version of the package. If the
  package is ever built as an XPI, this is used as the add-on's
  `em:version` element in its `install.rdf`.</p></td>
</tr>

<tr>
  <td id="dependencies"><code>dependencies</code></td>
  <td><p>a String or Array of Strings representing package
  names that this package requires in order to function properly.</p></td>
</tr>

<tr>
  <td id="lib"><code>lib</code></td>
  <td><p>a String representing the top-level module directory provided in
  this package. Defaults to `"lib"`.</p></td>
</tr>

<tr>
  <td id="tests"><code>tests</code></td>
  <td><p>a String representing the top-level module directory containing
  test suites for this package. Defaults to `"tests"`.</p></td>
</tr>

<tr>
  <td id="packages"><code>packages</code></td>
  <td><p>a String or Array of Strings representing paths to
  directories containing additional packages, defaults to
  `"packages"`.</p></td>
</tr>

<tr>
  <td id="main">main<code></code></td>
  <td><p>a String representing the name of a program module that is
  located in one of the top-level module directories specified by
  `lib`. Defaults to `"main"`.</p></td>
</tr>

<tr>
  <td id="harnessClassID"><code>harnessClassID</code></td>
  <td><p>a String in the GUID format:
  `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, where `x` represents a single
  hexadecimal digit. It is used as a `classID` (CID) of the "harness service"
  XPCOM component. Defaults to a random GUID generated by `cfx`.</p></td>
</tr>

<tr>
  <td id=""><code></code></td>
  <td><p></p></td>
</tr>

<tr>
  <td id=""><code></code></td>
  <td><p></p></td>
</tr>

</table>

