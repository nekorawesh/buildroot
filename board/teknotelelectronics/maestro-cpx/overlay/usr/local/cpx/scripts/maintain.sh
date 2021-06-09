#!/bin/bash
NET_SYS_CLASS_DIR="/sys/class/net"
NET_INTERFACE="eth0"
SERVICES_INIT_DIR="/etc/init.d"
NET_INIT_SCRIPT="S40network"

MQTT_HOST="localhost"
MQTT_TOPIC="maestro/hss/heartbeat"
declare -r MQTT_MAX_TRY=5
declare -i MQTT_MAX_WAIT=10
declare -i MQTT_ERR_CNTR=0

MQTT_MAX_WAIT=$((MQTT_MAX_TRY * 2))

declare -A SERVICES

SERVICES["watchdog"]="S15watchdog"
SERVICES["ntpd"]="S49ntp"
SERVICES["mosquitto"]="S50mosquitto"
SERVICES["redis-server"]="S50redis"
SERVICES["swupdate"]="S98swupdate"
SERVICES["dropbear"]="S50dropbear"
SERVICES["hss"]="S99hss"

isInterfaceUp() {
    ip link | grep -v '[0-9]: lo:' 2>/dev/null | grep -l '^[0-9].*.UP.*LOWER_UP' >/dev/null 2>&1
}

isNetworkUp() {
    ip route | grep '^default via ' 2>/dev/null | grep -lv 'linkdown' >/dev/null 2>&1
}

isInternetConnected() {
    if ! ping -c 3 8.8.8.8 >/dev/null 2>&1; then
        curl -Hfs www.google.com >/dev/null 2>&1 || return 1
    fi
    return 0
}

checkNetwork() {
    echo "Checking network..."
    if ! isInterfaceUp || ! isNetworkUp; then
        $SERVICES_INIT_DIR/$NET_INIT_SCRIPT start
    else
        if isInternetConnected; then
            echo "Interface ${NET_INTERFACE} up, internet connected."
        fi
    fi
}

checkServices() {
    echo "Checking apps and services..."
    for SERVICE in "${!SERVICES[@]}"; do
        echo "Checking $SERVICE"
        if pgrep -x "$SERVICE" >/dev/null; then
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
}

startHSS() {
    HSS_INIT_SCRIPT="$SERVICES_INIT_DIR/${SERVICES["hss"]}"
    if [ -f "$HSS_INIT_SCRIPT" ]; then
        $HSS_INIT_SCRIPT start
    else
        echo "hss init script not found!"
    fi
}

checkHSS() {
    echo "Checking hss app..."
    (MQTT_ERR_CNTR=0)
    for ((c = 0; c < $MQTT_MAX_TRY; c++)); do
        output=$(mosquitto_sub -h $MQTT_HOST -t $MQTT_TOPIC -C $MQTT_MAX_TRY -W $MQTT_MAX_WAIT | jq '.values.second' || exit 1)

        if [ -z "$output" ]; then
            ((MQTT_ERR_CNTR=MQTT_ERR_CNTR + 1))
        else
            for i in $(echo $output | tr " " "\n"); do
                if [[ $i < 0 || $i > 59 ]]; then
                    ((MQTT_ERR_CNTR=MQTT_ERR_CNTR + 1))
                else
                    (MQTT_ERR_CNTR=0)
                fi
            done
        fi
    done

    if [[ $MQTT_ERR_CNTR -ge $MQTT_MAX_TRY ]]; then
        (MQTT_ERR_CNTR=0)
        startHSS
    fi
}

maintain() {
    checkNetwork
    sleep 1
    checkServices
}

syncTime() {
    if isInternetConnected; then
        ntpdate -u pool.ntp.org
        /sbin/hwclock --systohc
    fi
}

case "$1" in
maintain | syncTime | checkHSS)
    "$1"
    ;;
*)
    echo "Usage: $0 {maintain|checkHSS|syncTime}"
    exit 1
    ;;
esac
