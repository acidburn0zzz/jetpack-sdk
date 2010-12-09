This section is a quick introduction to the modules that ship with the
SDK. It concentrates on the modules likely to be of most interest to add-on
developers, so most of the modules discussed here are from the `add-on-kit`
package.

## Building a UI ##

The SDK provides four modules to help you build a UI.

### [panel](#module/addon-kit/panel) ###

A panel is the SDK's version of a dialog. Its content is specified as HTML,
and it can be supplied with [content 
scripts](#guide/working-with-content-scripts) to interact with
the panel's content and send messages back to the main add-on code.

### [widget](#module/addon-kit/widget) ###

A widget is permanently displayed in a dedicated bar in the browser chrome.

Its content is specified as text or HTML, either passed directly into the
widget constructor or indirectly via a URL, it and can notify the add-on when
the user interacts with it by generating `click` and `mouseover`
[events](#guide/events). 

Widgets are generally used in one of two different contexts:

* to display compact content that should always be visible to the user, such as
the time in a selected time zone or the weather

* to provide a way for the user to access other parts of an add-on's user
interface. For example, a widget might open a settings dialog when the user
clicks it.

To simplify your code in the latter case, you can pass a panel object into the
widget's constructor, and the widget will display it on a click event. The
`reddit-panel` example demonstrates this.

### [context-menu](#module/addon-kit/panel) ###

We've already encountered the context menu module, which provides a mechanism
to add items and submenus to the browser's context menu.

### [notifications](#module/addon-kit/notifications) ###

This module enables an add-on to display transient messages to the user.

## Interacting With the Web ##

### [page-mod](#module/addon-kit/page-mod) ###

The page-mod module enables you to execute scripts in the context of selected
web pages, effectively rewriting the pages on the fly.

You supply a set of scripts to the page-mod and a [match 
pattern](#module/api-utils/match-pattern) which identifies, by URL, the pages
to which the scripts should be attached.

This is the module you should use if you need to modify web pages or simply to
retrieve content from pages the user visits.

### [page-worker](#module/addon-kit/page-mod) ###

Using a page worker an add-on can can load a page and access its content
without displaying it to the user.

### [request](#module/addon-kit/request) ###

We've already seen the request module, which enables you to make XML HTTP
(AJAX) requests from your add-on, and process the responses.

## Interacting With the Browser ##

### [clipboard](#module/addon-kit/clipboard) ###

The clipboard module enables you to get and set the contents of the system
clipboard.

### [private-browsing](#module/addon-kit/private-browsing) ###

 enables you
to start and stop private browsing mode, and be notified when the browser
transitions in and out of private browsing mode. You should use this module
if your add-on records anything which should not be recorded in private
browsing mode.

* ***[selection](#module/addon-kit/selection)***: get and set any selection
in the active page, either as text or HTML.

* ***[tabs](#module/addon-kit/tabs)***: this module enables you to interact
with the currently open tabs and to open new tabs. You can get the list of open
tabs and the current active tab, and get notified of changes to these. You can
Retrieve each tab and get certain information about it. Note that you can't
access the content hosted by the tab using this API.

* ***[windows](#module/addon-kit/windows)***: this module enables you to
interact with currently open windows and to open new windows. As for the `tabs`
module, you can get the list of open windows, the current active window, and
get notified of changes to these. You can retrieve each window and get certain
information about it. Again: you can't access the content hosted by the window
using this API.

### Utilities ###

<span class="aside">
This module needs much better documentation.
</span>

* ***[localization](#module/addon-kit/localization)***: helps you to support
multiple language variants for your add-on without needing to bundle localized
strings for all the languages with the add-on itself.

* ***[simple-storage](#module/addon-kit/simple-storage)***: provides your add-on with
persistent storage.

* ***[self](#module/jetpack-core/self)***: access to your add-on's [Program
ID](#guide/implementing) and any data bundled with your add-on: for example,
HTML content to be displayed in a user interface component or a content
script. Note that this module is in the 
[jetpack-core](#package/jetpack-core) package.

Next we will take a more detailed look at one of the basic idioms in the SDK:
the [Event Emitter framework](#guide/events).