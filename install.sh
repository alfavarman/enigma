#!/bin/bash

# Check if the user is in a virtual environment. If so, exit the script.
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "You are in a virtual environment. Please deactivate and run the script again. command: deactivate"
    exit 1
fi

# Remove old venv
if [ -d "venv" ]; then
    echo "Removing existing venv directory..."
    rm -rf venv
fi

# Create a new venv
echo "Creating a new virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements.
echo "Installing requirements..."
pip install -r backend/requirements.txt

# Navigate to the Django project directory.
cd backend/src/

# Run migrations.
echo "Running migrations..."
python manage.py migrate

# Create a superuser with the password 'admin'.
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Create Groups (Client & Seller) & permissions as per dosc/permissions.json
echo "Create Groups (Client & Seller) & permissions as per dosc/permissions.json"
python manage.py setup_groups_permissions

echo "-------------------------------------------------------"
echo "Installation Summary:"
echo "1. Virtual environment created and requirements installed."
echo "2. Database migrations applied."
echo "3. Superuser 'admin' created with password 'admin'."
echo "-------------------------------------------------------"
echo "To run the server, use the following command:"
echo "source venv/bin/activate && cd backend/src/ && python manage.py runserver"
