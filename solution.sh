#!/bin/bash

# Change the following values accordingly
HOST="127.0.0.1"
PORT="8080"

# Run the client script with provided arguments
python client.py --username YOUR_USERNAME signup
python client.py --username YOUR_USERNAME login

# Additional client actions here

chmod +x run_client.sh

./run_client.sh
