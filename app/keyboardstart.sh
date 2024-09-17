#!/bin/bash

# Check if wvkbd-mobintl is running
if pgrep -x "wvkbd-mobintl" > /dev/null
then
    echo "wvkbd-mobintl is already running."
else
    # Start wvkbd-mobintl with the desired options
    wvkbd-mobintl -L 300 -bg ff0000 --press ff00f0 --press-sp ff00f0 -O &
    echo "wvkbd-mobintl started."
fi
