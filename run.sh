#!/bin/bash
pip install --force dist/*.whl
flask --app employee_server run --debug
