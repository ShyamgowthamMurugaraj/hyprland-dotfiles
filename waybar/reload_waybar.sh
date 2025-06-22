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
echo "bad"
swaync-client -rs



echo "Reloading Waybar..."
if pgrep -x "waybar" > /dev/null; then
    pkill -SIGUSR2 waybar

    echo "Waybar reloaded successfully."
else
    echo "Warning: Waybar process not found. Skipping Waybar reload."
fi




