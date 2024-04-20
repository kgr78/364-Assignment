#!/bin/bash

# Change to the directory containing RipProtocol.py
cd /Users/isma/Desktop/COSC364/RIPAssignment/364-Assignment/src

# Array of config files
CONFIG_FILES=("config1.txt" "config2.txt" "config3.txt" "config4.txt" "config7.txt")

# Path to your Python script
PYTHON_SCRIPT="RipProtocol.py"

# Set the window size (optional)
WINDOW_WIDTH=800
WINDOW_HEIGHT=200

# Set the initial window position (optional)
WINDOW_X_POS=100
WINDOW_Y_POS=100

# Function to close all Terminal windows
close_terminals() {
    # Get the process IDs of all Terminal windows
    TERMINAL_PIDS=($(pgrep Terminal))
    
    # Close all Terminal windows
    for pid in "${TERMINAL_PIDS[@]}"; do
        kill -9 "$pid"
    done
}

# Loop to open a new Terminal window and run the Python script with each config file
for config_file in "${CONFIG_FILES[@]}"; do
    osascript -e "tell application \"Terminal\"
        activate
        do script \"cd /Users/isma/Desktop/COSC364/RIPAssignment/364-Assignment/src && python3 $PYTHON_SCRIPT $config_file\"
        set the bounds of the front window to {$WINDOW_X_POS, $WINDOW_Y_POS, $WINDOW_X_POS + $WINDOW_WIDTH, $WINDOW_Y_POS + $WINDOW_HEIGHT}
    end tell"
    sleep 1  # Optional delay between opening terminals
    
    # Calculate the new window position for the next iteration
    WINDOW_Y_POS=$((WINDOW_Y_POS + WINDOW_HEIGHT + 50))  # Adjust the vertical spacing as needed
done

# Wait for user to press 'q' key to close Terminal windows
echo "Press 'q' key to close all Terminal windows..."
while true; do
    read -n 1 key
    if [[ $key = "q" ]]; then
        break
    fi
done

close_terminals
