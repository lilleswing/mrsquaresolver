#!/bin/bash
virtualenv venv
source venv/bin/activate
pip install nose
nosetests --with-xunit tests
