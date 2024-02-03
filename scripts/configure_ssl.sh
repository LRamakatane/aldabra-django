#!/usr/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 4 ]; then
   echo "Usage: $0 SERVER_IP USER PUBLIC_KEY DOMAIN"
   exit 1
fi

# Assign arguments to variables
SERVER_IP="$1"
USER="$2"
PUBLIC_KEY="$3"
DOMAIN="$4"

ssh -i $PUBLIC_KEY $USER@$SERVER_IP "sudo apt-get update && sudo apt-get install certbot python3-certbot-nginx"
ssh -i $PUBLIC_KEY $USER@$SERVER_IP "sudo certbot --nginx -d $DOMAIN"
ssh -i $PUBLIC_KEY $USER@$SERVER_IP "sudo systemctl restart nginx"