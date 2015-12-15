# Flask demos

## Installation

Assuming you have cloned this repository already, on Ubuntu 15.04, install the following packages.

    apt-get install python3-flask python3-requests python3-requests-oauthlib

Or using a virtual environment:

    virtualenv -p /usr/bin/python3 env
    pip install flask requests requests-oauthlib


## Example 1: Plain OAuth 2.0 --- `example_basic.py`

This example demonstrates how to use Authentiq Connect with an existing OAuth 2.0 client library---requests-oauthlib in this case. It simply signs in using Authentiq and displays the retrieved user information.

## Example 2: Native Authentiq JS --- `example_native.py`

This example uses the [AuthentiqJS](https://github.com/AuthentiqID/authentiq-js) snippet for a richer authentication experience. In particular it shows the following features:

- A faster authentication flow using an OpenID Connect ID Token
- Instant sign-out from phone using the Authentiq ID app
