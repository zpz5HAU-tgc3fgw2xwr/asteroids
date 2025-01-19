#!/bin/bash

ENV_DIR=".venv"

# Check if the virtual environment exists
if [ ! -d "$ENV_DIR" ]; then
	echo "Virtual environment not found. Running setup..."
	python3 setup.py
fi

# Activate the virtual environment
if [ -f "$ENV_DIR/bin/activate" ]; then
	echo "Activating virtual environment..."
	source "$ENV_DIR/bin/activate"
else
	echo "Failed to find the virtual environment activation script. Please check your setup."
	exit 1
fi