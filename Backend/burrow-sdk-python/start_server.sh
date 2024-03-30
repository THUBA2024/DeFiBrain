#!/bin/sh

. ./venv/bin/activate
nohup python -u app.py > burrow.log 2>&1 &
