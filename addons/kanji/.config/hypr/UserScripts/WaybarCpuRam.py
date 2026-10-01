#!/usr/bin/env python3
"""Waybar custom/cpuram: a CPU and RAM pill, each line with a block-graph sparkline (Airy Aurora)."""
import json, os, re, signal, sys, time
from collections import deque

HISTORY = 120  # seconds kept, one sample per second
COLS, COL_SECONDS = 14, 3  # the pill graph: 14 columns of 3 s each
TIP_COLS = 60  # the tooltip graph spans all of HISTORY
BLOCKS = "▁▂▃▄▅▆▇█"
PALETTE = os.path.expanduser("~/.config/waybar/wallust/colors-waybar.css")
FALLBACK = {"color12": "#8CC0D6", "color13": "#D69CAC"}
_palette = [0, dict(FALLBACK)]


def colors():
    """CPU and RAM colors (color12, color13), re-read whenever wallust rewrites the palette."""
    try:
        mtime = os.stat(PALETTE).st_mtime
        if mtime != _palette[0]:
            css = open(PALETTE).read()
            found = dict(re.findall(r"@define-color (color1[23]) (#[0-9A-Fa-f]{6})", css))
            _palette[:] = [mtime, {**FALLBACK, **found}]
    except OSError:
        pass
    return _palette[1]["color12"], _palette[1]["color13"]


def spark(samples, cols, col_seconds):
    """One block per column, newest on the right; columns with no data yet stay blank."""
    out, n = [], len(samples)
    for c in range(cols):
        end = n - (cols - 1 - c) * col_seconds
        chunk = list(samples)[max(end - col_seconds, 0):max(end, 0)]
        out.append(BLOCKS[min(round(sum(chunk) / len(chunk) / 100 * 7), 7)] if chunk else " ")
    return "".join(out)


def cpu_times():
    fields = [int(x) for x in open("/proc/stat").readline().split()[1:]]
    return sum(fields), fields[3] + fields[4]  # total, idle + iowait


def memory():
    info = {k: int(v.split()[0]) for k, v in (l.split(":") for l in open("/proc/meminfo"))}
    total, used = info["MemTotal"], info["MemTotal"] - info["MemAvailable"]
    return used / total * 100, used / 1048576, total / 1048576


def line(name, pct, color, graph):
    return (f'<span foreground="{color}">{name} {pct:3d}%</span> '
            f'<span foreground="{color}" alpha="70%">{graph}</span>')


def render(cpu, ram, ram_used, ram_total, cpu_hist, ram_hist):
    c1, c2 = colors()
    pill = (f'<span font_size="75%" line_height="0.85">'
            f'{line("CPU", round(cpu), c1, spark(cpu_hist, COLS, COL_SECONDS))}\n'
            f'{line("RAM", round(ram), c2, spark(ram_hist, COLS, COL_SECONDS))}</span>')
    step = HISTORY // TIP_COLS
    tip = (f'<tt><span foreground="{c1}"><b>CPU {round(cpu)}%</b></span>  all cores\n'
           f'<span foreground="{c1}">{spark(cpu_hist, TIP_COLS, step)}</span>\n\n'
           f'<span foreground="{c2}"><b>RAM {round(ram)}%</b></span>  {ram_used:.1f} of {ram_total:.1f} GiB\n'
           f'<span foreground="{c2}">{spark(ram_hist, TIP_COLS, step)}</span>\n\n'
           f'<small>last {HISTORY // 60} min · click for btop</small></tt>')
    return pill, tip


def selftest():
    assert spark([], 4, 1) == "    "
    assert spark([0, 100], 4, 1) == "  ▁█"
    assert spark([50] * 8, 2, 4) == "▅▅"
    pill, tip = render(12.4, 55.0, 5.1, 31.2, deque([12]), deque([55]))
    assert "CPU  12%" in pill and "RAM  55%" in pill and "5.1 of 31.2 GiB" in tip
    print("ok")


def main():
    if "--test" in sys.argv:
        return selftest()
    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        signal.signal(sig, lambda *_: sys.exit(0))
    cpu_hist, ram_hist = deque(maxlen=HISTORY), deque(maxlen=HISTORY)
    prev_total, prev_idle = cpu_times()
    while True:
        time.sleep(1 - time.time() % 1)  # tick on the second
        total, idle = cpu_times()
        cpu = 100 * (1 - (idle - prev_idle) / max(total - prev_total, 1))
        prev_total, prev_idle = total, idle
        ram, ram_used, ram_total = memory()
        cpu_hist.append(cpu)
        ram_hist.append(ram)
        pill, tip = render(cpu, ram, ram_used, ram_total, cpu_hist, ram_hist)
        try:
            print(json.dumps({"text": pill, "tooltip": tip, "class": "cpuram"}), flush=True)
        except OSError:  # waybar closed the pipe
            return


if __name__ == "__main__":
    main()
