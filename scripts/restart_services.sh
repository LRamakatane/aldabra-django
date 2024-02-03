#!/bin/bash

sudo systemctl restart nginx
sudo systemctl restart daphne

echo "services restarted successfully!"