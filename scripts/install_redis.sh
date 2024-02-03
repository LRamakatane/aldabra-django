#!/usr/bin/bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis