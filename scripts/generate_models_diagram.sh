#!/bin/bash

# Generate models documentation for the network app

python manage.py graph_models themes -o clogs_theme_models.png
