#!/usr/bin/env bash
# WaybarCava.sh — safer single-instance handling, cleanup, and robustness
# Original concept by JaKooLit; this variant focuses on lifecycle hardening.

set -euo pipefail

# Ensure cava exists
if ! command -v cava >/dev/null 2>&1; then
  echo "cava not found in PATH" >&2
  exit 1
fi

# 0..15 → AiryBars font capsules (U+10F100+n, built by ~/.config/waybar/airybars/build.py)
bar=""; for n in $(seq 0 15); do bar+=$(printf "\U$(printf %08x $((0x10F100 + n)))"); done

RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp}"

# Unique temp config + cleanup on exit
config_file="$(mktemp "$RUNTIME_DIR/waybar-cava.XXXXXX.conf")"
cleanup() { kill ${cava_pid:-} ${awk_pid:-} 2>/dev/null || true; rm -f "$config_file"; }
trap cleanup EXIT INT TERM

cat >"$config_file" <<EOF
[general]
framerate = 60
bars = 10

[input]
method = pulse
source = auto

[output]
method = raw
raw_target = /dev/stdout
data_format = ascii
ascii_max_range = 15
EOF

# Airy Aurora: each bar gets one step of the blue→pink gradient (pastel, like the active workspace pill)
colors="#7AAFCA #82ADC6 #8AACC3 #91AABF #99A8BB #A1A7B8 #A9A5B4 #B0A3B0 #B8A2AD #C0A0A9"

# Stream cava output and translate digits 0..15 to colored bar glyphs
# waybar ignores SIGPIPE, so cava never exits on its own; awk does, then the EXIT trap kills cava
exec {cava_fd}< <(exec cava -p "$config_file")
cava_pid=$!
LC_ALL=C.UTF-8 awk -F';' -v bar="$bar" -v colors="$colors" '
  BEGIN { n = split(colors, col, " ") }
  { out = ""
    for (i = 1; i < NF; i++) out = out "<span font_family=\"AiryBars\" foreground=\"" col[(i - 1) % n + 1] "\">" substr(bar, $i + 1, 1) "</span>"
    if (out != last) { print out; fflush(); last = out } }' <&"$cava_fd" &
awk_pid=$!
wait "$awk_pid" || true
