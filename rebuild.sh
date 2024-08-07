#!/bin/bash
rm -rf dist
python -m build
pip install --force dist/*.whl
