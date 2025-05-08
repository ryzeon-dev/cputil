if [ "$(id -u)" != "0" ]; then
    echo "Must run as root"
    exit 1
fi

uninstallDaemon() {
    systemctl stop cputild
    systemctl disable cputild
    rm -rf /etc/cputild
}

uninstallBin() {
    rm -rf /usr/local/bin/cputil
}

if [ "$1" == "daemon" ]; then
    uninstallDaemon

elif [ "$1" == "bin" ]; then
    uninstallBin

elif [ "$1" == "all" ]; then
    uninstallDaemon
    uninstallBin

else
    echo "usage: uninstall.sh (daemon | bin | all)"
fi
