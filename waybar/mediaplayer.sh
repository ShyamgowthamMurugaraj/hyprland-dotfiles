while true; do
	player_status=$(playerctl -p spotify status 2>/dev/null)

	if [ "$player_status" = "Playing" ]; then
		artist=$(playerctl -p spotify metadata artist)
		title=$(playerctl -p spotify metadata title)
		# Escape special characters for JSON: ampersands and double quotes
		artist=$(echo "$artist" | sed 's/&/&amp;/g; s/"/\\"/g')
		title=$(echo "$title" | sed 's/&/&amp;/g; s/"/\\"/g')
		echo '{"text": "'"$artist - $title"'", "class": "custom-spotify", "alt": "Spotify"}'
	elif [ "$player_status" = "Paused" ]; then
		echo '{"text": "Paused", "class": "custom-spotify", "alt": "Spotify (Paused)"}'
	else
		echo '{"text":"Inactive", "class":"custom-spotify", "alt": "Spotify (Inactive)"}'
	fi
	sleep 1
done
