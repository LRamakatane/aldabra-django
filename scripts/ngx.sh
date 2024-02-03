#!/bin/bash

# # Check for correct number of arguments
# if [ "$#" -ne 2 ]; then
#   echo "Usage: $0 SERVER_IP PROJECT_FOLDER"
#   exit 1
# fi

# # Assign arguments to variables
# SERVER_IP="$1"
# PROJECT_FOLDER="$2"

# Run the command with sudo and redirect the input to the file
ENV="$ENV"
sudo cp -r /home/ubuntu/booking-$ENV/static/ /var/www/static/
sudo bash -c "echo '
server {
    server_name booking-api-$ENV.aajexpress.org;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        alias /var/www;
        expires 30d;
    }

    location / {
        include /etc/nginx/proxy_params;
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/booking-api-$ENV.aajexpress.org/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/booking-api-$ENV.aajexpress.org/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}


server {
    if (\$host = booking-api-$ENV.aajexpress.org) {
        return 301 https://\$host\$request_uri;
    } # managed by Certbot


    listen 80;
    server_name booking-api-$ENV.aajexpress.org;
    return 404; # managed by Certbot


}
' > /etc/nginx/sites-available/booking-api-$ENV"

# /etc/nginx/proxy_params

sudo bash -c "echo '
proxy_set_header X-Real-IP \$remote_addr;
proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto \$scheme;
' > /etc/nginx/proxy_params"


sudo ln -s /etc/nginx/sites-available/booking-api-$ENV /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx


echo "Nginx service file created successfully!"