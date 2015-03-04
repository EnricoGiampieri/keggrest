#!/bin/bash
python test_keggrest.py
python3 test_keggrest.py

coverage run test_keggrest.py
coverage report keggrest.py
coverage html -d coverage_html keggrest.py
