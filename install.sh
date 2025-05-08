if [ "$(id -u)" != "0" ]; then
    echo "Must run as root"
    exit 1
fi

makeVenv() {
    python3 -m venv venv
    source ./venv/bin/activate

    pip install pyinstaller
}

removeInstallFiles() {
    deactivate
    rm -rf ./build ./venv ./dist
}

installDaemon() {
    mkdir -p /etc/cputild/bin

    cp ./src/cputild.conf /etc/cputild
    cp ./src/cputild.service /etc/cputild

    pyinstaller --onefile ./src/cputild.py --name cputild
    cp ./dist/cputild /etc/cputild/bin
    rm -rf ./cputild.spec

    systemctl enable /etc/cputild/cputild.service 
    systemctl start cputild
}

installBin() {
    pyinstaller --onefile ./src/cputil.py --name cputil
    cp ./dist/cputil /usr/local/bin
    rm -rf ./cputil.spec 
}

if [ "$1" == "daemon" ]; then
    makeVenv
    installDaemon
    removeInstallFiles

elif [ "$1" == "bin" ]; then
    makeVenv
    installBin
    removeInstallFiles

elif [ "$1" == "all" ]; then
    makeVenv
    installDaemon
    installBin
    removeInstallFiles

else
    echo "usage: install.sh (daemon | bin | all)"
fi
