#!/bin/bash

# Generate models documentation for the network app

python manage.py graph_models network -o clogs_network_models.png
