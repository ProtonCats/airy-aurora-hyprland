#!/usr/bin/env bash
# Airy Aurora light/dark switch. Usage: airy.sh [light|dark|toggle] (default: toggle)
# light/dark: full apply (shared files, variant files, wallpaper). toggle: swap variant files only.
set -e
repo="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
env_conf="$HOME/.config/hypr/UserConfigs/ENVariables.conf"

# One switch at a time; a double click would otherwise race on the same files
exec 9>"${XDG_RUNTIME_DIR:-/tmp}/airy-aurora.lock"
flock -n 9 || exit 0

mode="${1:-toggle}"
full=1
if [ "$mode" = toggle ]; then
  full=
  grep -qs '^### Airy Aurora: dark' "$env_conf" && mode=light || mode=dark
fi
case "$mode" in
  light) scheme=airy-aurora; kitty_theme=airy-aurora.conf; gtk=Breeze ;;
  dark) scheme=airy-aurora-dark; kitty_theme=airy-aurora-dark.conf; gtk=Breeze-Dark ;;
  *) echo "usage: $0 [light|dark|toggle]" >&2; exit 2 ;;
esac

# Copy trees over $HOME; a replaced, different file gets a .bak-pre-airy copy, only the first time
install_tree() {
  cd "$repo/$1"
  find . \( -type f -o -type l \) -print0 | while IFS= read -r -d '' f; do
    dst="$HOME/${f#./}"
    mkdir -p "$(dirname "$dst")"
    [ -e "$dst" ] && [ ! -e "$dst.bak-pre-airy" ] && ! cmp -s "$f" "$dst" && cp -a "$dst" "$dst.bak-pre-airy"
    cp -a --remove-destination "$f" "$dst"
  done
}
if [ -n "$full" ]; then install_tree common; fi
install_tree "$mode"
mkdir -p "$HOME/.config/hypr/UserScripts"
ln -sfn "$repo/airy.sh" "$HOME/.config/hypr/UserScripts/AiryAurora.sh"

# GTK theme under Hyprland only; swaps out any earlier Airy Aurora block, other env lines are kept
if [ -f "$env_conf" ]; then
  sed -i -E '/^### Airy Aurora: (light|dark) GTK/d; /^env = GTK_THEME,Breeze(-Dark)?$/d; /^env = ADW_DEBUG_COLOR_SCHEME,prefer-(light|dark)$/d' "$env_conf"
  printf '### Airy Aurora: %s GTK in Hyprland only ###\nenv = GTK_THEME,%s\nenv = ADW_DEBUG_COLOR_SCHEME,prefer-%s\n' "$mode" "$gtk" "$mode" >> "$env_conf"
else
  echo "Note: $env_conf not found; skipped the GTK env lines (the waybar switch reads them to know the mode)." >&2
fi

if [ -n "$full" ]; then
  wall="$HOME/Pictures/wallpapers/4f3f3b208cbd6e98c69e32c612dd4f95.jpg"
  sw="$(command -v awww || command -v swww || true)"
  [ -n "$sw" ] && { "$sw" img "$wall" || true; }
fi
wallust cs -s "$HOME/.config/wallust/colorschemes/$scheme.json" || true
hyprctl reload >/dev/null || true
# Live env for apps launched from now on, so GTK follows without a relogin
hyprctl keyword env "GTK_THEME,$gtk" >/dev/null || true
hyprctl keyword env "ADW_DEBUG_COLOR_SCHEME,prefer-$mode" >/dev/null || true
# waybar/swaync restart from this shell, whose env predates the switch; their children (yad hints) inherit it
export GTK_THEME="$gtk" ADW_DEBUG_COLOR_SCHEME="prefer-$mode"
pkill -x waybar || true; setsid -f waybar >/dev/null 2>&1 9>&-
pkill -x swaync || true; setsid -f swaync >/dev/null 2>&1 9>&-
for s in /tmp/kitty*; do [ -S "$s" ] && kitty @ --to "unix:$s" set-colors -a -c "$HOME/.config/kitty/$kitty_theme" 2>/dev/null || true; done
echo "Airy Aurora ${mode^} applied."
