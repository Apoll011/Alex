#!/bin/bash

# Define constants
PID_FILE="/home/pegasus/.alex"
LOCATION="/bin/alex"

# Function to display usage information
usage() {
    echo "Usage: alex [options]"
    echo
    echo "Options:"
    echo "  install                                  Install Alex on this machine."
    echo "  -h/--help                                Display this help message."
    echo "  run                                      Run Alex with the following arguments:"
    echo "    --install-skill <file_path> <intent>   Install a skill from a file."
    echo "    -l, --language <language>              Set the language (choices: en, pt). Default: en."
    echo "    -b, --base-server <ip>                 Set the Base Server IP. Default: 127.0.0.1."
    echo "    -s, --start                            Start Alex."
    echo "    -d, --debug                            Enters Debug Mode."
    echo "    --voice                                Enters voice mode."
    echo "    -i, --interface <mode>                 Interface mode (choices: cmd, web, voice, api). Default: cmd."
    echo "    -h, --help                             Show help information."
    echo "    -v, --version                          Show version information."
    echo
    exit 0
}

# Run the Python script with arguments
run() {
  "$LOCATION" $@
}

install() {
  echo "Installing Alex..."
  mkdir /tmp/alex
  echo "Downloading Alex..."
  wget "http://0.0.0.0:1178/version_control/main/get" -O /tmp/alex/alex.zip -t 5 -q
  echo "Downloaded Alex..."
  echo "Building Alex..."
  unzip -qq /tmp/alex/alex.zip -d /tmp/alex/
  echo "Linking..."
  sudo cp /tmp/alex/main /bin/alex
  rm -r /tmp/alex
  echo "Alex Installed..."
}

uninstall(){
  sudo rm -f /bin/alex
  rm -r -f /home/pegasus/.alex_resources/
}

case "$1" in
    install)
        install
        ;;
    uninstall)
        uninstall
        ;;
    run)
        run "$@"
        ;;
    clear)
        clear
        ;;
    --help|-h)
        usage
        ;;
    *)
        echo "$1" is not a valid command. See -h/--help for help
        ;;
esac

