Welcome to the Add-on SDK.

The Add-on SDK is designed to make it easier to develop, test, package and
distribute Firefox and Thunderbird add-ons. It provides:

* a set of tools for creating, running, testing, and packaging add-ons. These
tools are made available through the `cfx` command-line interface.

* a set of modules providing a consistent set of high-level JavaScript APIs
which add-on developers can use to build user interfaces, interact with the
browser and with the Web.

This guide is intended to get you started using the SDK to develop add-ons.

After installing the SDK we will go through developing, running and packaging
a simple add-on, then go over the most commonly used APIs and some of the
programming techniques they use. Then we will put these together to show
how to build a more sophisticated add-on. Finally we will look at how you can
use the SDK not just to develop add-ons, but to develop your own modules that
extend the functionality of the SDK itself.

Prerequisites
-------------

To develop with the new Add-on SDK, you'll need:

<span class="aside">
Verify that Python is in your path.
</span>

* [Python] 2.5 or greater.

* A working version of Firefox, Thunderbird, or the [XULRunner SDK] that
  uses Gecko 1.9.2 or later (e.g., Firefox 3.6).

  [Python]: http://www.python.org/
  [XULRunner SDK]: https://developer.mozilla.org/en/Gecko_SDK

Installation
------------

At the time of this writing, the latest stable version of the Add-on
SDK is 0.10pre. You can obtain it as a [tarball] or a [zip file].

Alternatively, you can get the latest development version of the
Add-on SDK from its [HG repository].

Regardless of which option you choose, navigate to the root directory
of your checkout with a shell/command prompt. This directory should
be called `addon-sdk`.

<span class="aside">
Unlike many development tools, there isn't a system-wide location for
the Add-on SDK. Instead, developers can have as many installations of
the SDK as they want, each configured separately from one
another. Each installation is called a *virtual environment*.
</span>

Then, if you're on Linux, OS X, or another Unix-based system, run:

    source bin/activate

Otherwise, if you're on Windows, run:

    bin\activate

Now the beginning of your command prompt should contain the text
`(addon-sdk)`, which means that your shell has entered a special
virtual environment that gives you access to the Add-on SDK's
command-line tools.

At any time, you can leave a virtual environment by running
`deactivate`.

  [tarball]: https://ftp.mozilla.org/pub/mozilla.org/labs/jetpack/jetpack-sdk-latest.tar.gz
  [zip file]: https://ftp.mozilla.org/pub/mozilla.org/labs/jetpack/jetpack-sdk-latest.zip
  [HG repository]: http://hg.mozilla.org/labs/jetpack-sdk/

Sanity Check
------------

<span class="aside">
Unit and behavioral [testing] is something that
we're trying to make as easy and fast as possible in the Add-on SDK,
because it's imperative that we know when breakages occur between the
Mozilla platform and the SDK. We also need to make sure that creating
new functionality or modifying existing code doesn't break other
things.

  [testing]: http://www.mindview.net/WebLog/log-0025
</span>

Run this at your shell prompt:

    cfx

It should produce output whose first line looks something like this, followed by
many lines of usage information:

    Usage: cfx [options] [command]

This is the `cfx` command-line program.  It's your primary interface to the
Add-on SDK.  You use it to launch Firefox and test your add-on, package your
add-on for distribution, view documentation, and run unit tests.

Once you're ready, move on to the next section: [Implementing 
a simple add-on](#guide/implementing-simple).
