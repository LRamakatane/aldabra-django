#!/usr/bin/bash
# Check if the project folder argument is provided

Environment=$ENV

if [ $Environment = "staging" ]; then
   ip=***
   public_key="server-key-pair-staging.pem"

elif [ $Environment = "dev" ]; then
    ip=***
    public_key="server-key-pair.pem"

elif [ $Environment = "production" ]; then
    ip=***
    public_key="server-key-pair.pem"

else
    echo "can't get logs for that environment"
    exit 1
fi

ssh -i "$public_key" ubuntu@$ip