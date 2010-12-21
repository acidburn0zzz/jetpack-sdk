
# Module Development Guide #

The Module Development Guide explains how to use the low-level modules provided
by the SDK to build your own modules which implement new APIs for add-on code
to use, thus extending the SDK itself.

The [**Tutorials**](#guide/module-development/tutorials) section documents some
of the considerations involved in using the low-level modules. In particular,
it contains important information for people developing modules which require
privileged access to browser objects such as the chrome.

The [**Reference**](#guide/module-development/api-reference) section provides
detailed documentation for the low-level modules which you can use as building
blocks for your own modules. In particular, it contains modules that supply
basic services, like messaging, for higher-level modules. Many of these modules
require privileged access to the browser chrome.

The features and APIs in this Module Development guide, and the guide itself,
are still in active development, and we expect to make incompatible changes to
them in future releases.
