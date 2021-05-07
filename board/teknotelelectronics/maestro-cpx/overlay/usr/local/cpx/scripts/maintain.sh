#!/bin/bash

echo "Checking apps and services..."

SERVICES_INIT_DIR="/etc/init.d"

declare -A SERVICES

SERVICES["watchdog"]="S15watchdog"
SERVICES["ntpd"]="S49ntp"
SERVICES["mosquitto"]="S50mosquitto"
SERVICES["redis-server"]="S50redis"
SERVICES["swupdate"]="S98swupdate"
SERVICES["dropbear"]="S50dropbear"
SERVICES["hss"]="S99hss"

for SERVICE in "${!SERVICES[@]}"; do
    echo "Checking $SERVICE"
    if pgrep -x "$SERVICE" > /dev/null
    then
        echo "$SERVICE is running"
    else
        echo "$SERVICE stopped"
        SERVICE_INIT_SCRIPT="$SERVICES_INIT_DIR/${SERVICES[$SERVICE]}"
        if [ -f "$SERVICE_INIT_SCRIPT" ]; then
            $SERVICE_INIT_SCRIPT start
        else
            echo "$SERVICE init script not found!"
        fi
    fi
done

