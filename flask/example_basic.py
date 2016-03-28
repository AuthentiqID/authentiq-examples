#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask + Requests-OAuthlib example.

This example demonstrates how to integrate a server application with
Authentiq Connect, using standard OAuth 2.0. It uses the popular
requests-oauthlib module to make this trivial in Flask.

As with all plain OAuth 2.0 integrations, we use the UserInfo endpoint to
retrieve the user profile after authorization. Check out our native
AuthentiqJS snippet or an OpenID Connect library to optimise this.

"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import oauthlib
import requests

from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, session, url_for
from requests_oauthlib import OAuth2Session


class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = "Curve25519"

CLIENT_ID = "test-client-examples"
CLIENT_SECRET = "NoMorePassw0rds!"
REDIRECT_URL = "http://localhost:5555/authorized"
AUTHENTIQ_BASE = "https://connect.authentiq.io/"
AUTHENTIQ_BASE = "http://192.168.0.10:5000/"
AUTHORIZE_URL = AUTHENTIQ_BASE + "authorize"
TOKEN_URL = AUTHENTIQ_BASE + "token"
USERINFO_URL = AUTHENTIQ_BASE + "userinfo"

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def index():

    # Check if redirect_uri matches with the one registered with the
    # example client.
    assert url_for("authorized", _external=True) == REDIRECT_URL, (
        "For this demo to work correctly, please make sure it is hosted on "
        "localhost, so that the redirect URL is exactly " + REDIRECT_URL + "."
    )

    # Initialise an authentication session. Here we pass in scope and
    # redirect_uri explicitly, though when omitted defaults will be taken
    # from the registered client.
    authentiq = OAuth2Session(
        CLIENT_ID,
        scope=["openid", "aq:name", "aq:push"],
        redirect_uri=url_for("authorized", _external=True),
    )

    # Build the authorization URL and retrieve some client state.
    authorization_url, state = authentiq.authorization_url(AUTHORIZE_URL)

    # Save state to match it in the response.
    session["state"] = state

    # Redirect to the Authentiq Connect authentication endpoint.
    return redirect(authorization_url)


@app.route("/authorized")
def authorized():
    """
    OAuth 2.0 redirection point.
    """
    # Pass in our client side crypto state; requests-oauthlib will
    # take care of matching it in the OAuth2 response.
    authentiq = OAuth2Session(
        CLIENT_ID,
        state=session.get("state")
    )

    try:
        error = request.args["error"]
        oauthlib.oauth2.raise_from_error(error, request.args)
    except KeyError:
        pass
    except oauthlib.oauth2.OAuth2Error as e:
        code = e.status_code or 400
        description = "Provider returned: " + (e.description or e.error)
        abort(code, description=description)

    try:

        # Use our client_secret to exchange the authorization code for a
        # token. Requests-oauthlib parses the redirected URL for us.
        # The token will contain the access_token, a refresh_token, and the
        # scope the end-user consented to.
        token = authentiq.fetch_token(TOKEN_URL,
                                      client_secret=CLIENT_SECRET,
                                      authorization_response=request.url)

    # The incoming request looks flaky, let's not handle it further.
    except oauthlib.oauth2.OAuth2Error as e:
        abort(code=e.status_code or 400,
              description=e.description or e.error)

    # The HTTP request to the token endpoint failed.
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code or 502
        description = "Request to token endpoint failed: " + e.response.reason
        abort(code, description=description)


    # Now we can use the access_token to retrieve an OpenID Connect
    # compatible UserInfo structure from the provider. Once again,
    # requests-oauthlib adds a valid Authorization header for us.
    #
    # Note that this request can be optimized out if using an OIDC or
    # native Authentiq Connect client.
    try:
        userinfo = authentiq.get(USERINFO_URL).json()

    # The HTTP request to the UserInfo endpoint failed.
    except requests.exceptions.HTTPError as e:
        abort(
            code=e.response.status_code or 502,
            description="Request to userinfo endpoint failed: " +
                        e.response.reason
        )

    # Display the structure, use userinfo["sub"] as the user's UUID.
    return jsonify(userinfo)


if __name__ == "__main__":

    if app.debug:
        import os
        # Allow insecure oauth2 when debugging
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    app.run(port=5002)
