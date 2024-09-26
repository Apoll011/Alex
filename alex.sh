#!/bin/bash

# Define constants
PID_FILE="/home/pegasus/.alex"
SCRIPT_DIR="/home/pegasus/development/Alex"
LOG_FILE="output.log"

# Function to display usage information
usage() {
    echo "Usage: alex-frontend [options]"
    echo
    echo "Options:"
    echo "  --install-skill <file_path> <intent>    Install a skill from a file."
    echo "  -l, --language <language>             Set the language (choices: en, pt). Default: en."
    echo "  -b, --base-server <ip>                 Set the Base Server IP. Default: 127.0.0.1."
    echo "  -s, --start                            Start Alex."
    echo "  -d, --debug                            Enters Debug Mode."
    echo "  --voice                                Enters voice mode."
    echo "  -i, --interface <mode>                 Interface mode (choices: cmd, web, voice, api). Default: cmd."
    echo "  -v, --version                          Show version information."
    echo
    echo "The Alex front-end runs on the provided arguments."
    echo "Logs are saved to $LOG_FILE."
    exit 0
}

# Change to the script directory and activate the environment
cd "$SCRIPT_DIR" || { echo "Directory $SCRIPT_DIR does not exist."; exit 1; }
source .venv/bin/activate

# Run the Python script with arguments
run_python_script() {
    echo "Running Alex"
    python src/main.py "$@"
}

# Main script logic
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
else
    run_python_script "$@"
fi
