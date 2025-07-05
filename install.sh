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
    rm -rf ./build
}

installDaemon() {
    mkdir -p /etc/cputild/bin
    mkdir -p /etc/cputild/templates

    cp ./src/cputild.conf /etc/cputild
    cp ./src/cputild.service /etc/cputild

    mkdir -p ./build
    cd build

    cmake ../daemon_src
    make

    cp ./cputild /etc/cputild/bin
    cd ..

    systemctl enable /etc/cputild/cputild.service 
    systemctl start cputild
}

installBin() {
    mkdir -p ./build
    cd build

    makeVenv

    pyinstaller --onefile ../src/cputil.py --name cputil
    cp ./dist/cputil /usr/local/bin
    cd ..
}

if [ "$1" == "daemon" ]; then
    installDaemon
    removeInstallFiles

elif [ "$1" == "bin" ]; then
    installBin
    deactivate
    removeInstallFiles

elif [ "$1" == "all" ]; then
    installDaemon
    installBin
    deactivate
#    removeInstallFiles

else
    echo "usage: install.sh (daemon | bin | all)"
fi
