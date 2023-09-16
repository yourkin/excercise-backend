#!/usr/bin/env bash

# Network name
NETWORK_NAME="ex_back_shared_network"

# Check if the network exists
if docker network ls | grep -q $NETWORK_NAME; then
  echo "Network $NETWORK_NAME already exists, skipping creation."
else
  # Create the shared network
  docker network create $NETWORK_NAME
  echo "Network $NETWORK_NAME created."
fi
