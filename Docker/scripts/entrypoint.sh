#!/bin/bash

echo "Running container ..."

echo "Initializing IFPS node"

ipfs init

echo "Starting node exporter"

python3 python_scripts/node_exporter.py node1 &

echo "Starting ipfs daemon"

ipfs daemon &

sleep infinity

