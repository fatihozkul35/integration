.PHONY: help install run migrate makemigrations shell test clean superuser collectstatic build deploy-pa

# Default target
help:
	@echo "Django Project - Quick Commands"
	@echo "================================"
	@echo "install          - Install packages from requirements.txt"
	@echo "run              - Start development server"
	@echo "migrate          - Apply database migrations"
	@echo "makemigrations   - Create new migrations"
	@echo "migrateall       - Create and apply migrations (makemigrations + migrate)"
	@echo "shell            - Start Django shell"
	@echo "test             - Run tests"
	@echo "superuser        - Create superuser"
	@echo "collectstatic    - Collect static files"
	@echo "build            - Prepare for deployment (makemigrations + update requirements.txt)"
	@echo "deploy           - PythonAnywhere deployment (migrate + collectstatic)"
	@echo "clean            - Clean __pycache__ and .pyc files"
	@echo "venv             - Activate virtual environment (PowerShell)"
	@echo "format           - Format code (if black/autopep8 available)"
	@echo "testemail        - Test email sending with interactive script"
	@echo "sendtestemail    - Send test email using Django command (usage: make sendtestemail EMAIL=test@example.com)"

# Install packages
install:
	pip install -r requirements.txt

# Start development server
run:
	python manage.py runserver

# Apply migrations
migrate:
	python manage.py migrate

# Create new migrations
makemigrations:
	python manage.py makemigrations

# Create and apply migrations
migrateall:
	python manage.py makemigrations
	python manage.py migrate

# Django shell
shell:
	python manage.py shell

# Run tests
test:
	python manage.py test

# Create superuser
superuser:
	python manage.py createsuperuser

# Collect static files
collectstatic:
	python manage.py collectstatic --noinput

# Build - Pre-deployment commands (local build preparation)
# This command prepares the project for deployment:
# - Creates migration files
# - Updates requirements.txt with newly installed packages
# Uses a Python script for cross-platform compatibility
build:
	@python build_prepare.py || python3 build_prepare.py

# PythonAnywhere deployment - optimized for PythonAnywhere console
# This target is specifically designed for PythonAnywhere and uses python3.10
deploy:
	@echo "****************************************************************"
	@echo "PythonAnywhere Production Deployment"
	@echo "****************************************************************"
	@echo "Installing requirements..."
	@if [ -f venv/bin/python ]; then \
		venv/bin/python -m pip install -r requirements.txt; \
	elif command -v python3.10 >/dev/null 2>&1; then \
		python3.10 -m pip install -r requirements.txt; \
	elif command -v python3.9 >/dev/null 2>&1; then \
		python3.9 -m pip install -r requirements.txt; \
	else \
		python -m pip install -r requirements.txt; \
	fi
	@echo "Creating migration files..."
	@if [ -f venv/bin/python ]; then \
		venv/bin/python manage.py makemigrations; \
	elif command -v python3.10 >/dev/null 2>&1; then \
		python3.10 manage.py makemigrations; \
	elif command -v python3.9 >/dev/null 2>&1; then \
		python3.9 manage.py makemigrations; \
	else \
		python manage.py makemigrations; \
	fi
	@echo "Running database migrations..."
	@if [ -f venv/bin/python ]; then \
		venv/bin/python manage.py migrate; \
	elif command -v python3.10 >/dev/null 2>&1; then \
		python3.10 manage.py migrate; \
	elif command -v python3.9 >/dev/null 2>&1; then \
		python3.9 manage.py migrate; \
	else \
		python manage.py migrate; \
	fi
	@echo "Collecting static files..."
	@if [ -f venv/bin/python ]; then \
		venv/bin/python manage.py collectstatic --noinput; \
	elif command -v python3.10 >/dev/null 2>&1; then \
		python3.10 manage.py collectstatic --noinput; \
	elif command -v python3.9 >/dev/null 2>&1; then \
		python3.9 manage.py collectstatic --noinput; \
	else \
		python manage.py collectstatic --noinput; \
	fi
	@echo "****************************************************************"
	@echo "Deployment completed successfully!"
	@echo "Next steps:"
	@echo "  1. Go to PythonAnywhere dashboard"
	@echo "  2. Navigate to the 'Web' tab"
	@echo "  3. Click the 'Reload' button"
	@echo "****************************************************************"

# Clean cache files
clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Activate virtual environment (for PowerShell)
venv:
	@echo "To activate virtual environment: .\venv\Scripts\Activate.ps1"

# Format code (if black available)
format:
	black . 2>/dev/null || autopep8 --in-place --recursive . || echo "black or autopep8 not found"

# Test email sending with interactive script
testemail:
	python test_email.py

# Send test email using Django command
sendtestemail:
	@if [ -z "$(EMAIL)" ]; then \
		echo "Usage: make sendtestemail EMAIL=test@example.com"; \
	else \
		python manage.py sendtestemail $(EMAIL); \
	fi

