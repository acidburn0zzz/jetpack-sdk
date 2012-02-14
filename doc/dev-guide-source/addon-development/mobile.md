<div class="warning">Developing add-ons for Firefox Mobile is still
an experimental feature of the SDK: the APIs and cfx commands used
might change in future releases.</div>

# Developing for Firefox Mobile #

Mozilla has recently decided to
[reimplement the UI for Firefox Mobile on Android](http://starkravingfinkle.org/blog/2011/11/firefox-for-android-native-android-ui/)
 using native Android widgets instead of XUL. With the add-on SDK you
can develop add-ons that run on this new version of Firefox Mobile as
well as on the desktop version of Firefox.

You can use the same code to target both desktop Firefox and Firefox
Mobile, and just specify some extra options to `cfx run`, `cfx test`,
and `cfx xpi` when targeting Firefox Mobile.

Right now only the following modules are supported:

* page-mod
* page-worker
* request
* self
* simple-storage
* timers

We're working on adding support for the other modules.

This tutorial explains how to run SDK add-ons on an Android
device connected via USB to a development machine containing the SDK, using the
[Android Debug Bridge](http://developer.android.com/guide/developing/tools/adb.html)
to communicate between the SDK tools and the device.

<img class="image-center" src="static-files/media/mobile-setup-adb.png"/>

It's possible to use the
[Android emulator](http://developer.android.com/guide/developing/tools/emulator.html)
to develop add-ons for Android without access to a device, but it's slow,
so for the time being it's much easier to use the technique described
below.

## Setting up the Environment ##

First you'll need an
[Android device capable of running the native version of
Firefox Mobile](https://wiki.mozilla.org/Mobile/Platforms/Android#System_Requirements).
Then:

* install the
[Nightly build of the native version of Firefox Mobile](https://wiki.mozilla.org/Mobile/Platforms/Android#Download_Nightly)
on the device.
* [enable USB debugging on the device (step 3 of this link only)](http://developer.android.com/guide/developing/device.html#setting-up)

On the development machine:

* install version 1.5 or higher of the Add-on SDK
* install the correct version of the
[Android SDK](http://developer.android.com/sdk/index.html)
for your device
* using the Android SDK, install the
[Android Platform Tools](http://developer.android.com/sdk/installing.html#components)

Next, attach the device to the development machine via USB.

Now open up a command prompt. Android Platform Tools will have
installed an executable called `adb` in the "platform-tools"
directory under the directory in which you installed the Android
SDK. Make sure this directory is in your path. Then type:

<pre>
adb devices
</pre>

You should see some output like:

<pre>
List of devices attached 
51800F220F01564 device
</pre>

If you do, then `adb` has found your device and you can get started.
