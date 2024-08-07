#!/bin/bash
pip install '.[test]'
coverage run -m pytest
coverage report
