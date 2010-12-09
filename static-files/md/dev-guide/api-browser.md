## [clipboard](#module/addon-kit/clipboard) ##

The `clipboard` module enables you to get and set the contents of the system
clipboard.

## [private-browsing](#module/addon-kit/private-browsing) ##

`private-browsing` enables your add-on to start and stop private browsing mode,
and to be notified when the browser starts or stops private browsing
mode.

You should use these notifications to ensure your add-on respects private
browsing.

## [selection](#module/addon-kit/selection) ##

Using this module your add-on can get and set any selection in the active web
page, either as text or HTML.

## [tabs](#module/addon-kit/tabs) ##

This module enables you to interact with the currently open tabs and to open
new tabs.

You can get the list of open tabs and the current active tab, and get
notified of tabs opening, closing or becoming active and inactive.

You can retrieve each tab and get certain information about it such as its URL.

Note that you can't access the content hosted by the tab using this API.

## [windows](#module/addon-kit/windows) ##

Like the `tabs` module but for windows this module enables you to
interact with currently open windows and to open new windows.

You can get the list of open windows, the current
active window, and get notified of windows opening and closing, or becoming
active or inactive.

You can retrieve each window and get certain information about it such as the
list of tabs it hosts.

Again: you can't access the content hosted by the window using this API.

<br>
**Next**: [managing your add-on](#guide/api-managing).
