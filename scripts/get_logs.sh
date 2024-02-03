#!/usr/bin/bash
# Check if the sevice argument is provided
# for nginx=nginx
# for dahpne=booking-staging-daphne or booking-dev-daphne

Environment=$ENV

if [ "$#" -ne 1 ]; then
   echo "Usage: $0 service"
   exit 1
fi

if [ $Environment = "staging" ]; then
   ip=54.209.231.42
   public_key="server-key-pair-staging.pem"

elif [ $Environment = "dev" ]; then
    ip=34.192.156.241
    public_key="server-key-pair.pem"

elif [ $Environment = "production" ]; then
    ip=54.243.217.35
    public_key="server-key-pair.pem"

else
    echo "can't get logs for that environment"
    exit 1
fi

SERVICE="$1"

ssh -i "$public_key" ubuntu@$ip "sudo journalctl -u $SERVICE -f"

ssh -i "$public_key" ubuntu@$ip "sudo journalctl -u $SERVICE -f"
