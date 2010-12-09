The SDK provides four modules to help you build a UI.

## [panel](#module/addon-kit/panel) ##

A panel is the SDK's version of a dialog. Its content is specified as HTML,
and it can be supplied with [content
scripts](#guide/web-content) to interact with
the panel's content and send messages back to the main add-on code.

You can use a panel anywhere your application needs to display a dialog.

## [widget](#module/addon-kit/widget) ##

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

Like the panel, the widget uses [content scripts](#guide/web-content) to
interact with the content it hosts.

## [context-menu](#module/addon-kit/panel) ##

The context menu module lets you add items and submenus to the browser's
context menu.

You can define the context in which the item is shown using any
of a number of predefined contexts (for example, when some content on the page
is selected) or define your own contexts using scripts.

You can use [content scripts](#guide/web-content) to interact with the page.

## [notifications](#module/addon-kit/notifications) ##

This module enables an add-on to display transient messages to the user.

<br>
**Next**: [interacting with the web](#guide/api-web).
