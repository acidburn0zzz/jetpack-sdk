<!-- contributed by Irakli Gozalishvili [gozala@mozilla.com]  -->

The `passwords` module allows add-ons to interact with the host application's
built-in password management system, in order to:

1. Retrieve credentials for a website, to access the user's account on the
   website and retrieve information about the user.
2. Securely store credentials that are associated with the add-on, to access
   them in subsequent sessions.
3. Store credentials that are associated with a particular website so that both
   add-on and the user (when visiting the site without the add-on) can access
   them in subsequent sessions.

<api name="search">
@function

This function is used to locate a credential stored in the host application's
built-in login management system.

** Searching for credentials associated with an add-on **

    require("passwords").search({
      realm: "{{add-on}} Login",
      onComplete: function onComplete(credentials) {
        // credentials is an array of all credentials
        // with a given `realm`.
        credentials.forEach(function(credential) {
          // Your logic goes here.
        });
      }
    });

** Searching for credentials associated with a given user name **

    require("passwords").search({
      username: "jack",
      onComplete: function onComplete(credentials) {
        // credentials is an array of all credentials
        // with a given `username`.
        credentials.forEach(function(credential) {
          // Your logic goes here.
        });
      }
    });

** Searching for credentials associated with a given web page **

    require("passwords").search({
      url: "http://www.example.com",
      onComplete: function onComplete(credentials) {
        // credentials is an array of all credentials
        // associated with the supplied url.
        credentials.forEach(function(credential) {
          // Your logic goes here.
        });
      }
    });

** Combining search terms together **

    require("passwords").search({
      url: "http://www.example.com",
      username: "jack",
      realm: "Login",
      onComplete: function onComplete(credentials) {
        // credentials is an array of all credentials
        // associated with given url, realm, and user name
        credentials.forEach(function(credential) {
          // Your logic goes here.
        });
      }
    });

@param options {object}
An object containing fields associated with a credential being searched. It may
contain any combination of the following fields:

* `username`
* `password`,
* `realm`
* `url`
* `usernameField`
* `passwordField`

All these fields are described in detail under the `store` section. Any
supplied fields are used as search terms to narrow down the search results.

This parameter must contain an `onComplete` callback property which will be
called with an array of matched credentials.

</api>

<api name="store">
@function 

This function is used to store credentials in the host
application's built-in login manager.

It takes an `options` object as an
argument: this contains the containing fields needed to create a login
credential.

** Storing a credential associated with an add-on**

Add-ons may store credentials that are not associated with any web sites.
In this case the `realm` string briefly denotes the login's purpose.

    require("passwords").store({
      realm: "User Registration",
      username: "joe",
      password: "SeCrEt123",
    });

** Storing a credential associated with a web page **

Most sites use HTML form login based authentication. The following example
stores a credential for such a web site:

    require("passwords").store({
      url: "http://www.example.com",
      formSubmitURL: "http://login.example.com",
      username: "joe",
      usernameField: "uname",
      password: "SeCrEt123",
      passwordField: "pword"
    });

This login would correspond to a form on "http://www.example.com/login" with
the following HTML:

    <form action="http://login.example.com/foo/authenticate.cgi">
          <div>Please log in.</div>
          <label>Username:</label> <input type="text" name="uname">
          <label>Password:</label> <input type="password" name="pword">
    </form>

** Storing a site authentication login **

Some web sites use HTTP/FTP authentication. The associated credentials
contain different fields:

    require("passwords").store({
      url: "http://www.example.com",
      realm: "ExampleCo Login",
      username: "joe",
      password: "SeCrEt123",
    });

This would correspond to a login on "http://www.example.com" when the server
sends a reply such as:

    HTTP/1.0 401 Authorization Required
    Server: Apache/1.3.27
    WWW-Authenticate: Basic realm="ExampleCo Login"

If the website does not include the `realm` string in the `WWW-Authenticate`
header, then the `realm` property must be omitted.

Which properties are valid for `options` depends on the type of
authentication, but regardless of that there are two optional callback
`onComplete` and `onError` properties that may be passed to observe the
success or failure of the operation.

@param options {object}
An object containing fields associated with a credential being created and
stored. Some fields are necessary for one type of authentication and not
for another. Please see examples to find more details.

@prop username {string}
The user name for the login.

@prop password {string}
The password for the login.

@prop [url] {string}
The `url` to which the login applies, formatted as a URL (for example,
"http://www.site.com"). A port number (":123") may be appended.

_Please note: `http`, `https` and `ftp` URLs should not include path from the
full URL, it will be stripped out if included._

@prop [formSubmitURL] {string}
The URL a form-based login was submitted to.

For logins obtained from HTML forms, this field is the `action` attribute
from the form element, with the path removed
(for example, "http://www.site.com").

Forms with no `action` attribute default to submitting to their origin URL, so
that should be stored here. (`formSubmitURL` should not include the path from
the full URL, it will be stripped out if included).

@prop [realm] {string}
The HTTP Realm for which the login was requested.

When an HTTP server sends a 401 result, the WWW-Authenticate header includes a
realm to identify the "protection space": see
[RFC 2617](http://tools.ietf.org/html/rfc2617).

If the result did not include a realm, then this option must be omitted.
For logins obtained from HTML forms, this field must be omitted. 

For credentials associated with add-ons this field briefly denotes the
credential's purpose. It will be displayed as a description in the
application's built-in login management UI.

@prop [usernameField] {string}
The `name` attribute for the user name input in a form. Non-form logins
must omit this field.

@prop [passwordField] {string}
The `name` attribute for the password input in a form. Non-form logins
must omit this field.

@prop  [onComplete] {function}
The callback function that is called once the credential is stored.

@prop [onError] {function}
The callback function that is called if storing a credential failed. The
function is passed an `error` containing a reason of a failure.

</api>

<api name="remove">
@function

Remove a stored credential.

** Removing a credential **

    require("passwords").search({
      url: "http://www.example.com",
      username: "joe",
      onComplete: function onComplete(credentials) {
        credentials.forEach(require("passwords").remove);
      })
    });

** Changing a credential **

To change an existing credential just call `store` after `remove` succeeds:

    require("passwords").remove({
      realm: "User Registration",
      username: "joe",
      password: "SeCrEt123"
      onComplete: function onComplete() {
        require("passwords").store({
          realm: "User Registration",
          username: "joe",
          password: "{{new password}}"
        })
      }
    });

@param options {object}
When removing a credential the specified `options` object must exactly match
what was stored (including a `password`). For this reason it is recommended to
chain this function with `search` to make sure that only necessary matches are
removed.

</api>
