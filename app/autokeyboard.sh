#!/bin/bash

# Function to start the virtual keyboard
start_keyboard() {
    if ! pgrep -x "wvkbd-mobintl" > /dev/null
    then
        wvkbd-mobintl -L 300 -bg ff0000 --press ff00f0 --press-sp ff00f0 -O &
        echo "Keyboard started."
    fi
}

# Function to stop the virtual keyboard
stop_keyboard() {
    if pgrep -x "wvkbd-mobintl" > /dev/null
    then
        sudo pkill wvkbd-mobintl
        echo "Keyboard stopped."
    fi
}

# Monitor focus changes
while true; do
    # Get the currently focused window
    FOCUSED_WINDOW=$(xdotool getwindowfocus)

    # Get the window class to check what kind of application is focused
    WIN_CLASS=$(xprop -id "$FOCUSED_WINDOW" WM_CLASS)

    # If a terminal is focused, trigger the keyboard
    if [[ "$WIN_CLASS" =~ "Terminal" ]] || [[ "$WIN_CLASS" =~ "XTerm" ]]; then
        echo "Terminal window focused."
        start_keyboard
    else
        # For other windows, check if they support text input
        if xprop -id "$FOCUSED_WINDOW" | grep -q "input"; then
            echo "Text input field detected."
            start_keyboard
        else
            echo "No input field detected."
            stop_keyboard
        fi
    fi

    # Poll every second
    sleep 1
done
