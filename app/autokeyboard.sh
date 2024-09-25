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

# Monitor focus changes using xprop
while true; do
    # Get the current focused window ID
    FOCUSED_WINDOW_HEX=$(xprop -root _NET_ACTIVE_WINDOW | awk '{print $NF}')
    
    # Ensure the window ID is valid
    if [[ "$FOCUSED_WINDOW_HEX" != "0x0" ]] && [[ -n "$FOCUSED_WINDOW_HEX" ]]; then
        FOCUSED_WINDOW=$(printf "%d\n" "$FOCUSED_WINDOW_HEX")
        
        # Check if the focused window is valid and has input fields (like a text box)
        if xprop -id "$FOCUSED_WINDOW" | grep -q "WM_CLASS"; then
            if xprop -id "$FOCUSED_WINDOW" | grep -q "input"; then
                echo "Input field focused."
                start_keyboard
            else
                echo "No input field focused."
                stop_keyboard
            fi
        else
            stop_keyboard
        fi
    else
        stop_keyboard
    fi
    
    # Polling every second
    sleep 1
done
