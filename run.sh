#!/bin/bash
rm -rf dist
python -m build
pip install --force dist/*.whl
flask --app employee_server run --debug --no-reload
