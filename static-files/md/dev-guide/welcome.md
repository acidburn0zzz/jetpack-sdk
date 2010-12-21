# Add-on Development Made Easy #

The Add-on SDK is designed to make it easy to develop Firefox add-ons. It
includes:

* A set of **high-level modules** providing JavaScript APIs which you can
use to create add-ons. These modules simplify tasks such as building a user
interface and interacting with the Web, and will help ensure your add-on
continues to work as new versions of Firefox are released.

* A set of **tools** for creating, running, testing, and packaging add-ons.

Start with the [**Tutorials**](#guide/addon-development/tutorials): they
explain how to install the SDK, take you through the process of writing a
simple add-on and introduce the main APIs.

The [**Reference**](#guide/addon-development/api-reference) section
provides detailed documentation for the high-level APIs and tools in the SDK.

You can browse example add-ons in the
[**Examples**](#guide/addon-development/examples) section.

There are some features which are potentially useful to add-on developers,
but are not yet stabilized, and which we do expect to change in incompatible
ways in the future. We have documented these features in a separate
[**Experimental**](#guide/addon-development/experimental) section.

# Create Your Own APIs #

You're not limited to the high-level APIs. The SDK also includes a
collection of modules which you can use to create your own high-level modules,
extending the SDK APIs. The [**Module
Development**](#guide/module-development/about) guide explains how to do this.
