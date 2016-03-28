#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import io
import json
import logging
import multiprocessing
import os
import pytest
import requests
import signal
import time

from flask import url_for

from example_basic import app

logging.basicConfig(level=logging.DEBUG)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@pytest.yield_fixture(scope="session")
def running_app():
    """
    Start a Flask app in a separate process; yield process and request context.
    """
    app.config.update({
        "SERVER_NAME": "127.0.0.1:5002",
        "TESTING": True,
        "DEBUG": False
    })

    process = multiprocessing.Process(target=app.run)
    process.daemon = True
    process.start()
    time.sleep(0.2)
    with app.test_request_context():
        yield process
    os.kill(process.pid, signal.SIGINT)
    process.join()


@pytest.fixture
def mocked_userinfo(monkeypatch):
    """
    Mocked UserInfo endpoint.
    """
    def mock_request(self, method, url, *args, **kwargs):
        userinfo = {
            "name": "Demo User"
        }
        response = requests.Response()
        response.status_code = 200
        response.raw = io.BytesIO(json.dumps(userinfo))
        return response

    monkeypatch.setattr("requests.sessions.Session.request", mock_request)


def test_app_runs(running_app):
    assert running_app
    assert running_app.is_alive()


def test_index(running_app):

    url = url_for("index", _external=True)

    # check we are redirected to provider
    res = requests.get(url, allow_redirects=False)
    print(res.content)
    assert res.status_code == 302

    # load provider authorization page
    url = res.headers.get("Location")
    res = requests.get(url, allow_redirects=False)
    print(res.content)
    assert res.status_code == 200
    print(dict(res.headers))
    assert res.headers


def test_authorized(running_app):
    """
    Test if app displays the user information after authorization.
    """
    url = url_for("authorized", code="1234", _external=True)
    res = requests.get(url, allow_redirects=False)
    assert res.status_code == 200
    data = res.json()
    print(data)
    assert data["name"] == "Demo User"
