#!/bin/bash

# Get the project folder from the first command-line argument
PROJECT_FOLDER=aldabra-$ENV
PORT=8000

# # Check if the project folder argument is provided
# if [ -z "$PROJECT_FOLDER" ]; then
#   echo "Error: Project folder not provided."
#   echo "Usage: ./myscript.sh <project_folder>"
#   exit 1
# fi

# Generate the contents of the gunicorn.service file
SERVICE_CONTENT="[Unit]
Description=Daphne Service for Your aldabra API
After=network.target

[Service]
WorkingDirectory=$HOME/$PROJECT_FOLDER
Environment=DJANGO_SETTINGS_MODULE=config.settings
ExecStart=$HOME/$PROJECT_FOLDER/venv/bin/daphne -p $PORT -b 127.0.0.1 ws:app --verbosity 2
User=ubuntu
Restart=always

[Install]
WantedBy=multi-user.target"

WORKER_CONTENT="[Unit]
Description=Your Django App Worker
After=network.target

[Service]
WorkingDirectory=$HOME/$PROJECT_FOLDER
ExecStart=$HOME/$PROJECT_FOLDER/venv/bin/python $HOME/$PROJECT_FOLDER/manage.py runworker payment_status shipment_status
User=ubuntu
Restart=always

[Install]
WantedBy=multi-user.target"

# Create the gunicorn.service file with the generated contents
echo "$SERVICE_CONTENT" | sudo tee /etc/systemd/system/aldabra-$ENV-daphne.service > /dev/null
echo "$WORKER_CONTENT" | sudo tee /etc/systemd/system/aldabra-$ENV-worker.service > /dev/null

# Reload systemd to pick up the changes
sudo systemctl daemon-reload
sudo systemctl start aldabra-$ENV-daphne
sudo systemctl enable aldabra-$ENV-daphne
sudo systemctl restart aldabra-$ENV-daphne

sudo systemctl daemon-reload
sudo systemctl start aldabra-$ENV-worker
sudo systemctl enable aldabra-$ENV-worker
sudo systemctl restart aldabra-$ENV-worker


echo "Daphne service file created successfully!"