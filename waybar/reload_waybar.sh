#!/bin/bash

WALL_DIR="$HOME/Pictures/wallpapers"

CWD="$(pwd)"

cd "$WALL_DIR" || exit

IFS=$'\n'

SELECTED_WALL=$(for a in *.jpg *.jpeg *.png; do echo -en "$a\0icon\x1f$a\n"; done | rofi -dmenu -p "Choose Wallpaper")

echo "$SELECTED_WALL"


swww img "$SELECTED_WALL" --transition-type center

wal -i "$SELECTED_WALL"

pywalfox update
swaync-client -rs




# Find the Process ID (PID) of the Waybar instance
WAYBAR_PID=$(pgrep waybar)

# Check if Waybar is running
if [ -z "$WAYBAR_PID" ]; then
    echo "Waybar is not running."
    exit 1
fi

# Send the SIGUSR1 signal to Waybar to reload its configuration
# SIGUSR1 is signal number 10, but 'USR1' is more readable.
pkill -USR1 "$WAYBAR_PID"

echo "Waybar reloaded."

