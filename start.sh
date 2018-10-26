#!/bin/bash
cd web
# python main.py
gunicorn app:app -k gevent -b 0.0.0.0:5000