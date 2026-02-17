if [ "$(id -u)" != "0" ]; then
    echo "Must run as root"
    exit 1
fi

makeVenv() {
    echo 'Creating python virtual environment for compilation'
    python3 -m venv venv
    source ./venv/bin/activate

    pip install pyinstaller
}

removeInstallFiles() {
    echo 'Removing temp files'
    rm -rf ./build
}

installDaemon() {
    echo 'Creating configuration directories'
    mkdir -p /etc/cputild/templates

    cp ./src/cputild.conf /etc/cputild
    cp ./src/cputild.service /etc/cputild

    echo 'Compiling daemon'
    mkdir -p ./build
    cd build

    cmake ../daemon_src
    make

    echo 'Installing daemon'
    cp ./cputild /usr/loca/bin/
    cd ..

    echo 'Enabling and starting daemon service'
    systemctl enable /etc/cputild/cputild.service 
    systemctl start cputild
}

installBin() {

    mkdir -p ./build
    cd build

    makeVenv
    echo 'Installing python dependencies into venv'
    pip install pyyaml

    echo 'Compiling python binary'
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
    removeInstallFiles

else
    echo "usage: install.sh (daemon | bin | all)"
fi
