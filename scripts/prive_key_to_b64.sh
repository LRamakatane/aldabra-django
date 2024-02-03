#!/usr/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 1 ]; then
   echo "Usage: $0 PRIVATE_KEY"
   exit 1
fi

# Assign arguments to variables
PRIVATE_KEY="$1"

base64 -w 0 < $PRIVATE_KEY