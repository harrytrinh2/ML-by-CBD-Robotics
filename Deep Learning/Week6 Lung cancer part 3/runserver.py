#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import argparse

from uploadr.app import app

parser = argparse.ArgumentParser(description="Uploadr")
parser.add_argument(
    "--port", "-p",
    type=int,
    help="Port to listen on",
    default=1996,
)
args = parser.parse_args()

if __name__ == '__main__':
    flask_options = dict(
        debug=True,
        port=args.port,
        threaded=True,
    )

    app.run(**flask_options)

