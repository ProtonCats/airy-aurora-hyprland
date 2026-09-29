# Airy Aurora Switch — Hyprland Dots Theme

[Airy Aurora Light](https://github.com/ProtonCats/airy-aurora-light) and [Airy Aurora Dark](https://github.com/ProtonCats/airy-aurora-dark) in one repo, with a waybar button that flips between them. It's built for [KooL Hyprland](https://github.com/JaKooLit/Hyprland-Dots) (dots v2.3.20, Hyprland 0.56).

## Install

```bash
./airy.sh light    # or: ./airy.sh dark
```

A full apply copies `common/` and the chosen variant over your home directory. Any file it replaces is first saved as `<name>.bak-pre-airy`, but only the first time and only when the old file is different. The script then sets the wallpaper and palette, reloads Hyprland, restarts waybar and swaync, and recolors open kitty windows. It also links itself to `~/.config/hypr/UserScripts/AiryAurora.sh`, which is what the waybar button runs, so re-run it if you move this repo.

## Switch

- **Waybar:** KooL's light/dark button (`custom/light_dark`, in the menu drawer) now runs the toggle instead of `DarkLight.sh`. Its icon shows the current mode: 󰖨 for light, 󰖔 for dark. Middle click and right click still open the wallpaper and waybar style menus.
- **Terminal:** `./airy.sh` or `./airy.sh toggle`.

A toggle copies only the variant files, so it keeps whatever wallpaper you have set. It works out the current mode from the Airy Aurora GTK block in `~/.config/hypr/UserConfigs/ENVariables.conf`. It rewrites that block and also pushes it live with `hyprctl keyword env`, so GTK apps you open afterwards match the new mode without logging out. GTK apps that are already open keep their old theme until you restart them. A lock stops a double click from running two switches at once.

**Needs:** Hyprland, KooL dots, waybar, swaync, rofi, hyprlock, kitty, wallust, awww (or swww), and the fonts JetBrainsMono Nerd Font and Victor Mono.

## Layout

| Path | Contents |
|---|---|
| `common/` | Files that are the same in both modes: waybar `ModulesCustom`, `WaybarCava.sh`, `WaybarPlayerGradient.py`, `WindowRules.conf`, wallpaper |
| `light/` | Light palette, waybar style, kitty theme, hyprlock, swaync, rofi, decorations and the wallust-calling scripts |
| `dark/` | The same set for dark |

The palettes, kitty settings and per-file details are documented in the two variant repos linked above.

## Notes

- `wallust cs` gets the full path to the scheme file (`~/.config/wallust/colorschemes/airy-aurora[-dark].json`). Passed by name only, wallust errors out with "many matches" when a similarly named file such as a backup sits next to the scheme. The wallpaper scripts (`scripts/WallustSwww.sh` and `UserScripts/WallpaperEffects.sh`) do the same, so picking a new wallpaper keeps the palette of the current mode.
- KooL upgrades overwrite `scripts/` and `waybar/ModulesCustom`. Re-run `./airy.sh light` or `./airy.sh dark` after one.
- Don't use KooL's `DarkLight.sh`, because it fights the fixed palette.
