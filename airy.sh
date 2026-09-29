#!/usr/bin/env bash
# Airy Aurora light/dark switch. Usage: airy.sh [light|dark|toggle] (default: toggle) | airy.sh kanji on|off
# light/dark: full apply (shared + variant files). toggle: swap variant files only. kanji: optional waybar add-on.
set -e
repo="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
env_conf="$HOME/.config/hypr/UserConfigs/ENVariables.conf"
kanji_state="${XDG_STATE_HOME:-$HOME/.local/state}/airy-aurora/kanji"

# One switch at a time; a double click would otherwise race on the same files
exec 9>"${XDG_RUNTIME_DIR:-/tmp}/airy-aurora.lock"
flock -n 9 || exit 0

mode="${1:-toggle}"
full=1
if [ "$mode" = toggle ] || [ "$mode" = kanji ]; then
  full=
  grep -qs '^### Airy Aurora: dark' "$env_conf" && cur=dark || cur=light
  if [ "$mode" = toggle ]; then [ "$cur" = dark ] && mode=light || mode=dark; fi
fi
case "$mode" in
  light) scheme=airy-aurora; kitty_theme=airy-aurora.conf; gtk=Breeze ;;
  dark) scheme=airy-aurora-dark; kitty_theme=airy-aurora-dark.conf; gtk=Breeze-Dark ;;
  kanji) [ "$cur" = dark ] && gtk=Breeze-Dark || gtk=Breeze ;;
  *) echo "usage: $0 [light|dark|toggle] | $0 kanji on|off" >&2; exit 2 ;;
esac

# Copy trees over $HOME; a replaced, different file gets a .bak-<suffix> copy, only the first time
install_tree() {
  local bak="${2:-pre-airy}"
  cd "$repo/$1"
  find . \( -type f -o -type l \) -print0 | while IFS= read -r -d '' f; do
    dst="$HOME/${f#./}"
    mkdir -p "$(dirname "$dst")"
    [ -e "$dst" ] && [ ! -e "$dst.bak-$bak" ] && ! cmp -s "$f" "$dst" && cp -a "$dst" "$dst.bak-$bak"
    cp -a --remove-destination "$f" "$dst"
  done
}

restart_waybar() {
  # From this shell, whose env may predate a switch; waybar's children (yad hints) inherit it
  export GTK_THEME="$gtk" ADW_DEBUG_COLOR_SCHEME="prefer-$1"
  pkill -x waybar || true; setsid -f waybar >/dev/null 2>&1 9>&-
}

# Kanji add-on: on installs addons/kanji; off puts back the Airy copy (common/) or the pre-add-on backup
if [ "$mode" = kanji ]; then
  case "$2" in
    on)
      install_tree addons/kanji pre-kanji
      mkdir -p "$(dirname "$kanji_state")"; touch "$kanji_state" ;;
    off)
      [ -e "$kanji_state" ] || { echo "Airy kanji add-on is not on." >&2; exit 1; }
      cd "$repo/addons/kanji"
      find . -type f -print0 | while IFS= read -r -d '' f; do
        dst="$HOME/${f#./}"
        if [ -e "$repo/common/$f" ]; then cp -a --remove-destination "$repo/common/$f" "$dst"; rm -f "$dst.bak-pre-kanji"
        elif [ -e "$dst.bak-pre-kanji" ]; then mv -f "$dst.bak-pre-kanji" "$dst"
        else rm -f "$dst"
        fi
      done
      rm -f "$kanji_state" ;;
    *) echo "usage: $0 kanji on|off" >&2; exit 2 ;;
  esac
  fc-cache -f "$HOME/.local/share/fonts" >/dev/null 2>&1 || true
  restart_waybar "$cur"
  echo "Airy kanji add-on $2."
  exit 0
fi

if [ -n "$full" ]; then
  install_tree common
  # common/ carries the plain ModulesCustom, so an enabled add-on goes back on top of it
  [ -e "$kanji_state" ] && install_tree addons/kanji pre-kanji
fi
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

wallust cs -s "$HOME/.config/wallust/colorschemes/$scheme.json" || true
hyprctl reload >/dev/null || true
# Live env for apps launched from now on, so GTK follows without a relogin
hyprctl keyword env "GTK_THEME,$gtk" >/dev/null || true
hyprctl keyword env "ADW_DEBUG_COLOR_SCHEME,prefer-$mode" >/dev/null || true
restart_waybar "$mode"
pkill -x swaync || true; setsid -f swaync >/dev/null 2>&1 9>&-
for s in /tmp/kitty*; do [ -S "$s" ] && kitty @ --to "unix:$s" set-colors -a -c "$HOME/.config/kitty/$kitty_theme" 2>/dev/null || true; done
# Starship prompt, only if its config defines the matching palette (see README)
star="$HOME/.config/starship.toml"
grep -qs "^\[palettes\.${scheme//-/_}\]" "$star" && sed -i "s/^palette = .*/palette = \"${scheme//-/_}\"/" "$star"
echo "Airy Aurora ${mode^} applied."
