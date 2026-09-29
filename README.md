# Airy Aurora Hyprland

A frosted, pastel rice for [KooL Hyprland](https://github.com/JaKooLit/Hyprland-Dots) (dots v2.3.20, Hyprland 0.56). It comes in light and dark modes, and one key or a waybar button switches between them. Each mode uses a fixed palette, so changing the wallpaper doesn't recolor everything.

![Airy Aurora Hyprland, dark mode](docs/screenshot.jpg)

<sub>Wallpaper not included. It's a photograph whose original source hasn't been identified; if it's your work, please open an issue so it can be credited.</sub>

## Install

```bash
./airy.sh light    # or: ./airy.sh dark
```

A full apply copies `common/` and the chosen mode's files over your home directory. Any file it replaces is first saved as `<name>.bak-pre-airy`, but only the first time and only when the old file is different. The script then applies the palette, reloads Hyprland, restarts waybar and swaync, and recolors open kitty windows. It also links itself to `~/.config/hypr/UserScripts/AiryAurora.sh`, which the switch runs, so re-run it if you move this repo.

The palette doesn't depend on the wallpaper, so any image works. Set one with KooL's wallpaper menu (<kbd>SUPER</kbd> + <kbd>W</kbd>).

**Needs:** Hyprland, KooL dots, waybar, swaync, rofi, hyprlock, kitty, wallust, and the fonts JetBrainsMono Nerd Font and Victor Mono.

## Switch

- **Keybind:** <kbd>SUPER</kbd> + <kbd>ALT</kbd> + <kbd>D</kbd>. The installer doesn't add this. Put the line below in `~/.config/hypr/UserConfigs/UserKeybinds.conf`, which KooL upgrades leave alone:

  ```
  bindd = $mainMod ALT, D, Toggle Airy Aurora light/dark, exec, $HOME/.config/hypr/UserScripts/AiryAurora.sh toggle
  ```

- **Waybar:** KooL's light/dark button (`custom/light_dark`, in the menu drawer) runs the toggle instead of `DarkLight.sh`. Its icon shows the current mode: 󰖨 for light, 󰖔 for dark. Middle click and right click still open the wallpaper and waybar style menus.
- **Terminal:** `./airy.sh` or `./airy.sh toggle`.

A toggle copies only the files for the new mode, so your wallpaper stays as it is. It works out the current mode from the Airy Aurora GTK block in `~/.config/hypr/UserConfigs/ENVariables.conf`. It rewrites that block and also pushes it live with `hyprctl keyword env`, so GTK apps you open afterwards match the new mode without logging out. Waybar and swaync are restarted with the new values too, so windows they open (like the HINT! quick tips) follow the mode. GTK apps that are already open keep their old theme until you restart them. A lock stops a double click from running two switches at once.

## Kanji add-on (optional)

A calmer waybar with Japanese icons. It's off by default.

```bash
./airy.sh kanji on     # ./airy.sh kanji off to undo
```

- **Icons:** single kanji replace the icon glyphs: 時 clock, 網 network (断 when down), 算 CPU, 記 RAM, 盤 disk, 強/中/弱 power profile, 音 volume (静 when muted), 光/夕 night light, 錠 lock, and 昼/夜 for the light/dark button. In the menu drawer, 書 is files, 端 terminal, 覧 browser, 設 settings and 新 dots update. Three spots get drawn motifs from the bundled AiryJP font: a narutomaki swirl for the app menu, sushi for notifications (crossed out in do-not-disturb), and a torii gate for power.
- **Less clutter:** the weather shows only the temperature, and the weather kanji (晴 月 曇 雨 雪 雷) appear in its tooltip. The CPU temperature leaves the hardware drawer, and the HINT! and idle-inhibitor buttons are removed from the `[TOP] Default` layout. <kbd>SUPER</kbd> + <kbd>H</kbd> still opens the hints.
- **How it installs:** it copies `addons/kanji/` over your home directory: waybar `Modules`, `ModulesCustom`, `ModulesGroups` and `configs/[TOP] Default`, KooL's `Weather.py`, `WeatherWrap.sh` and `Hyprsunset.sh`, and the font to `~/.local/share/fonts/AiryJP/`. Replaced files are saved as `<name>.bak-pre-kanji`. A marker in `~/.local/state/airy-aurora/kanji` keeps it on through later full applies. `off` puts back Airy's `ModulesCustom` and the saved originals, and removes the font.
- **Needs:** a Japanese CJK font. Kanji fall back to it through fontconfig, and Noto Sans CJK JP gives the Japanese glyph forms (Fedora: `google-noto-sans-cjk-fonts`).
- **Font source:** `addons/kanji-font/build.py` draws every icon as SVG strokes and builds `AiryJP.ttf` into the add-on (needs Inkscape, fontTools, cairosvg and Pillow). It has 31 icons, including unused ones like a koi, lantern and wind chime, and `build.py preview` renders a sheet of them all. Icons map to U+10F000 onward in list order, so add new ones at the end.

## Palette

| Role | Light | Dark |
|---|---|---|
| Background | `#EEF2F6` haze | `#1B1E26` night ink |
| Foreground | `#30343D` ink | `#E3E9EF` haze |
| Soft panel | `#DDE6EE` | `#262B35` |
| Accent (ice) | `#AACCDD` | `#AACCDD` |
| Accent (blush) | `#CCB2B9` | `#CCB2B9` |
| Accent (steel / teal) | `#9CB9C9` | `#6A96A3` |
| Deep accent / cursor | `#4F7C8B` | `#8CC0D6` |
| Muted | `#767C85` | `#8A919C` |
| Media text gradient | `#7AAFCA` → `#C0A0A9` | `#7AAFCA` → `#C0A0A9` |

Dark-mode text colors are at least 5:1 contrast against the background. The full 16-color palettes are in `light/.config/wallust/colorschemes/airy-aurora.json` and `dark/.config/wallust/colorschemes/airy-aurora-dark.json`.

## What it themes

- **Hyprland** (`UserDecorations.conf`): gaps 5 inside and 10 outside, rounding 12. The active border is a 45° `#AACCDD` → `#9CB9C9` → `#CCB2B9` gradient. Inactive windows are at 0.94 opacity with no dimming. Blur size 8, vibrancy 0.18; brightness is 1.05 in light mode and 0.85 in dark. `WindowRules.conf` blurs the bar.
- **Waybar:** frosted pills (`style/[Light] Airy Aurora.css` or `style/[Dark] Airy Aurora.css`). The active workspace has a pastel `#AACCDD` → `#CCB2B9` pill. The music visualizer and song title get a per-character pastel gradient, colored by `scripts/WaybarCava.sh` and `UserScripts/WaybarPlayerGradient.py`.
- **Kitty:** `kitty.conf` includes `airy-aurora.conf` or `airy-aurora-dark.conf` at 0.85 background opacity, with JetBrainsMono Nerd Font 12, a blinking beam cursor with a trail, and a powerline tab bar at the bottom. The dark theme brightens the 16 ANSI colors so they stay readable. In both themes the ANSI blue and magenta are tinted toward the ice and blush accents, so tools like fastfetch that use ANSI colors match the rice.
- **Starship (optional):** if `~/.config/starship.toml` has a `[palettes.airy_aurora]` or `[palettes.airy_aurora_dark]` table, the switch sets `palette =` to the matching one. The palette needs these names: `crust surface0 surface2 overlay1 text lavender teal red peach yellow`. `kitty.conf` is global, so this applies in every desktop session, not just Hyprland.
- **GTK:** Breeze or Breeze-Dark, plus a libadwaita light/dark preference, under Hyprland only.
- **Also themed:** hyprlock (dark mode dims the wallpaper to 55%), the swaync notification center, and the rofi launcher.

## Layout

| Path | Contents |
|---|---|
| `common/` | Files that are the same in both modes: waybar `ModulesCustom`, `WaybarCava.sh`, `WaybarPlayerGradient.py`, `WindowRules.conf` |
| `light/` | Light palette, waybar style, kitty theme, hyprlock, swaync, rofi, decorations and the wallust-calling scripts |
| `dark/` | The same set for dark |
| `addons/kanji/` | The optional kanji add-on, installed by `./airy.sh kanji on` |
| `addons/kanji-font/` | Source for the add-on's AiryJP icon font |

## Notes

- Every `wallust cs` call gets the full path to the scheme file. Given only a name, wallust errors out with "many matches" when a similarly named file, such as a backup, sits next to the scheme. The wallpaper scripts (`scripts/WallustSwww.sh` and `UserScripts/WallpaperEffects.sh`) do the same, so picking a new wallpaper keeps the current mode's palette.
- KooL upgrades overwrite `scripts/` and `waybar/ModulesCustom`. Re-run `./airy.sh light` or `./airy.sh dark` after one; that also re-applies the kanji add-on if it's on. The add-on's copies of KooL files come from dots v2.3.20, so after an upgrade that changes them, turning the add-on on would bring back the older versions.
- Don't use KooL's `DarkLight.sh`, because it fights the fixed palette.
