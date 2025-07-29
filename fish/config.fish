
if status is-interactive
    # Commands to run in interactive sessions can go here
end

set -g fish_greeting

if test -e ~/.cache/wal/colors.fish
   source ~/.cache/wal/colors.fish
end

starship init fish | source

#source (wal --print-result | psub)

#neofetch

# Created by `pipx` on 2025-07-24 16:10:46
set PATH $PATH /home/rxdiationx/.local/bin
