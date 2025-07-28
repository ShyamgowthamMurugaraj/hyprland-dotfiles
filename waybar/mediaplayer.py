#!/usr/bin/env python3

import subprocess
import json
import time
import sys

# Configuration for scrolling and player checks
MAX_DISPLAY_LENGTH = 20  # Maximum characters to display in Waybar. Text will be padded or scrolled to this length.
SCROLL_SPEED = 1         # How many characters to advance the scroll position per update
SCROLL_INTERVAL = 0.1    # Time between each scroll update (in seconds). Smaller values make scrolling smoother.
PLAYER_CHECK_INTERVAL = 0.1 # How often to check Spotify player status and metadata (in seconds).

def get_spotify_status():
    """Fetches the current status of the Spotify player."""
    try:
        # Run playerctl to get the status
        result = subprocess.run(
            ['playerctl', '-p', 'spotify', 'status'],
            capture_output=True,
            text=True,
            check=False # Do not raise an exception for non-zero exit codes (e.g., player not running)
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            # Player might not be running or Spotify might not be open
            return "Stopped"
    except FileNotFoundError:
        print("Error: playerctl not found. Please ensure it is installed and in your PATH.", file=sys.stderr)
        return "Error"
    except Exception as e:
        print(f"An unexpected error occurred while getting status: {e}", file=sys.stderr)
        return "Error"

def get_spotify_metadata():
    """Fetches the artist and title metadata from Spotify."""
    artist = "Unknown Artist"
    title = "Unknown Title"
    try:
        # Get artist
        artist_result = subprocess.run(
            ['playerctl', '-p', 'spotify', 'metadata', 'artist'],
            capture_output=True,
            text=True,
            check=False
        )
        if artist_result.returncode == 0:
            artist = artist_result.stdout.strip()

        # Get title
        title_result = subprocess.run(
            ['playerctl', '-p', 'spotify', 'metadata', 'title'],
            capture_output=True,
            text=True,
            check=False
        )
        if title_result.returncode == 0:
            title = title_result.stdout.strip()

    except FileNotFoundError:
        pass # Error already reported by get_spotify_status
    except Exception as e:
        print(f"An unexpected error occurred while getting metadata: {e}", file=sys.stderr)

    return artist, title

def main():
    full_track_info = ""
    scroll_position = 0
    player_current_status = "Inactive"
    last_player_check_time = time.time()
    # New variables to store the last known artist and title for comparison
    last_known_artist = ""
    last_known_title = ""

    count=0
    while True:
        count+=1
        current_time = time.time()

        # Check player status and update full_track_info less frequently
        if current_time - last_player_check_time >= PLAYER_CHECK_INTERVAL:
            new_player_status = get_spotify_status()
            
            # Flag to determine if track info needs to be updated
            needs_track_info_update = False

            if new_player_status == "Playing":
                # Always fetch metadata if playing to check for song change
                current_artist, current_title = get_spotify_metadata()
                
                # Update if status changed OR if artist/title changed while still playing
                if new_player_status != player_current_status or \
                   current_artist != last_known_artist or \
                   current_title != last_known_title:
                    needs_track_info_update = True
                    last_known_artist = current_artist
                    last_known_title = current_title
            else: # Paused or Stopped/Inactive
                # Update if status changed (e.g., from Playing to Paused/Stopped)
                if new_player_status != player_current_status:
                    needs_track_info_update = True
                    last_known_artist = "" # Clear last known track for non-playing states
                    last_known_title = ""

            if needs_track_info_update:
                player_current_status = new_player_status
                if player_current_status == "Playing":
                    # Use the freshly fetched artist/title
                    full_track_info = f"{last_known_artist} - {last_known_title}"
                    scroll_position = 0  # Reset scroll position for new track
                elif player_current_status == "Paused":
                    full_track_info = "Paused"
                    scroll_position = 0  # Reset scroll position for static text
                else: # Stopped or Error
                    full_track_info = "Inactive"
                    scroll_position = 0  # Reset scroll position for static text
            
            last_player_check_time = current_time

        # Determine the text to display based on player status and scrolling logic
        display_text = ""
        tooltip_text = full_track_info # Tooltip always shows the full info
        scrollable_content=""
        if player_current_status == "Playing":
            if len(full_track_info) > MAX_DISPLAY_LENGTH:
                if scrollable_content:
                    scrollable_content=list(scrollable_content)
                    del scrollable_content[:start_index]
                    scrollable_content="".join(scrollable_content)
                print(scrollable_content)
                # Create a scrollable string by repeating the info and adding a separator
                # This ensures enough content to slice without index errors and for wrapping effect
                scrollable_content = full_track_info + "   " # Add some spaces for separation
                scrollable_content = scrollable_content * count # Repeat to ensure continuous scroll
                
                # Get the current segment for display, ensuring it's MAX_DISPLAY_LENGTH long
                start_index = scroll_position % len(scrollable_content)
                display_text = scrollable_content[start_index : start_index + MAX_DISPLAY_LENGTH].ljust(MAX_DISPLAY_LENGTH)
                
                # Update scroll position
                scroll_position = (scroll_position + SCROLL_SPEED)
            else:
                # Text is short enough, no scrolling needed. Pad with spaces to MAX_DISPLAY_LENGTH.
                display_text = full_track_info
            
            # Construct dictionary for JSON output
            output_data = {
                "text": display_text,
                "class": "custom-spotify",
                "alt": "Spotify",
                "tooltip": tooltip_text
            }
        elif player_current_status == "Paused":
            # Pad "Paused" to MAX_DISPLAY_LENGTH
            output_data = {
                "text": "Paused",
                "class": "custom-spotify",
                "alt": "Spotify (Paused)",
                "tooltip": "Spotify (Paused)"
            }
        else: # Inactive, Stopped, or Error
            # Pad "Inactive" to MAX_DISPLAY_LENGTH
            output_data = {
                "text": "Inactive",
                "class": "custom-spotify",
                "alt": "Spotify (Inactive)",
                "tooltip": "Spotify (Inactive)"
            }
        
        # Print the JSON string to standard output
        print(json.dumps(output_data))
        sys.stdout.flush() # Ensure the output is immediately sent

        # Sleep for the scroll interval to control update frequency
        time.sleep(SCROLL_INTERVAL)

if __name__ == "__main__":
    main()
