# Third Party Modules #

The SDK is extensible by design: any developer can build reusable modules
which fill gaps in the SDK's supported APIs, and these modules can be used
by other add-on developers in exactly the same way they use supported APIs.

In this example we'll use Erik Vold's
[`menuitems`](https://github.com/erikvold/menuitems-jplib) module to add a menu
item to Firefox's Tools menu.

## Installing `menuitems` ##

First we'll download `menuitems` from
[https://github.com/erikvold/menuitems-jplib](https://github.com/erikvold/menuitems-jplib). Like [addon-kit](packages/addon-kit/addon-kit.html) and
[api-utils](packages/api-utils/api-utils.html), it's a
[CommonJS package](dev-guide/addon-development/commonjs.html),
so we'll extract it under the SDK's `packages` directory:

<pre>
(addon-sdk)~/addon-sdk > cd packages
(addon-sdk)~/addon-sdk/packages > tar -xf ../erikvold-menuitems-jplib-d80630c.zip
</pre>

Now if you run `cfx docs` you'll see the `menuitems` package appearing
in the sidebar alongside `addon-kit`. Click on it and you'll see basic
information about the package, and any documentation that the package
author has provided.

The basic information is taken from the package's
[`package.json`](dev-guide/addon-development/package-spec.html) file. The page
for `menuitems` includes one especially interesting line:

<pre>
Dependencies             api-utils, vold-utils
</pre>

This tells us that we need to find the `vold-utils` package and install it.
We find that [here](https://github.com/erikvold/vold-utils-jplib),
download it, and add it under the `packages` directory alongside `menuitems`.

## Using `menuitems` ##

We can use the `menuitems` module in exactly the same way we use built-in
modules.

The documentation for the `menuitems` module tells us to we create a menu
item using `MenuItem()`. Of the options accepted by `MenuItem()`, we'll use
this minimal set:

* `id`: identifier for this menu item
* `label`: text the item displays
* `command`: function called when the user selects the item
* `menuid`: identifier for the item's parent element
* `insertbefore`: identifier for the item before which we want our item to
appear

Create a new directory and run `cfx init` in it. Open `lib/main.js` and
replace its contents with this:

    var menuitem = require("menuitems").Menuitem({
      id: "clickme",
      menuid: "menu_ToolsPopup",
      label: "Click Me!",
      onCommand: function() {
        console.log("clicked");
      },
      insertbefore: "menu_pageInfo"
    });

Next, we have to declare our dependency on the `menuitems` package.
In your add-on's `package.json` add the line:

<pre>
"dependencies": "menuitems"
</pre>

Note that due to
[bug 663480](https://bugzilla.mozilla.org/show_bug.cgi?id=663480), if you
add a `dependencies` line to `package.json`, and you use any modules from
built-in packages like [`addon-kit`](packages/addon-kit/addon-kit.html), then
you must also declare your dependency on that built-in package, like this:

<pre>
"dependencies": ["menuitems", "addon-kit"]
</pre>

Now we're done. Run the add-on and you'll see the new item appear in the
`Tools` menu: select it and you'll see `info: clicked` appear in the
console.

## Caveats ##

Eventually we expect the availability of a rich set of third party modules
will be one of the most valuable aspects of the SDK. Right now they're a great
way to use features not supported by the supported APIs without the
complexity of using the low-level APIs, but our support for third party
modules is still fairly immature.

* It's not always obvious where to find third-party modules, although some
are collected in the [Jetpack Wiki](https://wiki.mozilla.org/Jetpack/Modules).
* Third party modules typically require high security privileges, which
increases the damage a malicious web site could do if it were able to
compromise your add-on.
* Because third party modules typically use low-level APIs, they may be broken
by new releases of Firefox. In particular, many third party modules will be
broken by the
[multiple process architecture](https://wiki.mozilla.org/Electrolysis/Firefox)
(Electrolysis) planned for Firefox.
