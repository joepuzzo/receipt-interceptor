#!/bin/bash

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Check if brctl is installed
if ! command -v brctl &> /dev/null; then
    echo "brctl could not be found, please install bridge-utils"
    exit 1
fi

# Create the bridge br0
brctl addbr br0

# Bring down eth0 and eth1
ifconfig eth0 down
ifconfig eth1 down

# Add eth0 and eth1 to the bridge br0
brctl addif br0 eth0
brctl addif br0 eth1

# Bring eth0, eth1, and br0 up
ifconfig eth0 up
ifconfig eth1 up
ifconfig br0 up

# Show bridge info
brctl show

# Show IP address info
ip addr show

