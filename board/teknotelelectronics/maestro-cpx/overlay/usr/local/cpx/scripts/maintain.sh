#!/bin/bash
NET_SYS_CLASS_DIR="/sys/class/net"
NET_INTERFACE="eth0"
SERVICES_INIT_DIR="/etc/init.d"
NET_INIT_SCRIPT="S40network"

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
maintain | syncTime)
    "$1"
    ;;
*)
    echo "Usage: $0 {maintain|syncTime}"
    exit 1
    ;;
esac
