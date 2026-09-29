#!/usr/bin/env python3
"""Waybar custom/playerctl: "artist  title" colored blue→pink per character (Airy Aurora)."""
import ctypes, html, json, signal, subprocess, sys

BLUE, PINK = (0x7A, 0xAF, 0xCA), (0xC0, 0xA0, 0xA9)
MAX_CHARS = 25


def gradient(text):
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS - 1] + "…"
    out, n = [], max(len(text) - 1, 1)
    for i, ch in enumerate(text):
        rgb = (round(b + (p - b) * i / n) for b, p in zip(BLUE, PINK))
        out.append('<span foreground="#%02X%02X%02X">%s</span>' % (*rgb, html.escape(ch)))
    return "".join(out)


def main():
    fmt = "{{artist}}\t{{title}}\t{{playerName}}\t{{status}}"
    # PR_SET_PDEATHSIG (1): playerctl gets SIGTERM if this script dies by any signal
    die_with_parent = lambda: ctypes.CDLL("libc.so.6").prctl(1, signal.SIGTERM)
    proc = subprocess.Popen(["playerctl", "-a", "metadata", "--format", fmt, "-F"],
                            stdout=subprocess.PIPE, text=True, preexec_fn=die_with_parent)
    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        signal.signal(sig, lambda *_: sys.exit(0))
    try:
        for line in proc.stdout:
            artist, title, player, status = (line.rstrip("\n").split("\t") + [""] * 4)[:4]
            text = f"{artist}  {title}" if artist else title
            print(json.dumps({"text": gradient(text) if text.strip() else "",
                              "tooltip": html.escape(f"{player} : {title}"),
                              "alt": status, "class": status}), flush=True)
    except BrokenPipeError:
        pass
    finally:
        proc.terminate()


if __name__ == "__main__":
    main()
