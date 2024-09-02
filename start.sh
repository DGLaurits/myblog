#!/bin/bash
echo Starting Flask app.
cd /var/www/flask
source .venv/bin/activate
gunicorn -w 2 -b 127.0.0.1:8080 app:app
