## [page-mod](#module/addon-kit/page-mod) ##

The `page-mod` module enables you to execute scripts in the context of selected
web pages, effectively rewriting the pages inside the browser.

You supply a set of scripts to the page-mod and a [`match
pattern`](#module/api-utils/match-pattern) which identifies, by URL, a set of
web pages. When the user visits these pages the scripts are attached and
executed.

This is the module you should use if you need to modify web pages or simply to
retrieve content from pages the user visits.

## [page-worker](#module/addon-kit/page-mod) ##

Using a page worker, an add-on can load a page and access its DOM without
displaying it to the user.

## [request](#module/addon-kit/request) ##

This module enables you to make XML HTTP (AJAX) requests from your
add-on, and process the responses.

<br>
**Next**: [interacting with the browser](#guide/api-browser).
