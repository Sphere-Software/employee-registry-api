#!/bin/bash
pip install '.[test]'
coverage run -m pytest --junit-xml=test-results.xml
coverage report
