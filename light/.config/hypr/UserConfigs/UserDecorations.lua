-- Converted from UserDecorations.conf (hyprlang -> Lua)

S("wallust/wallust-hyprland")
hl.config({
    general = {
        border_size = 2,
        gaps_in = 5,
        gaps_out = 10,
        col = {
            active_border = { colors = { "rgba(AACCDDee)", "rgba(9CB9C9ee)", "rgba(CCB2B9ee)" }, angle = 45 },
            inactive_border = "rgba(DDE6EE66)",
        },
    },
    decoration = {
        rounding = 12,
        active_opacity = 1.0,
        inactive_opacity = 0.94,
        fullscreen_opacity = 1.0,
        dim_inactive = false,
        dim_special = 0.3,
        shadow = {
            enabled = true,
            range = 18,
            render_power = 3,
            color = "rgba(30343D22)",
            color_inactive = "rgba(30343D11)",
        },
        blur = {
            enabled = true,
            size = 8,
            passes = 3,
            new_optimizations = true,
            xray = true,
            ignore_opacity = true,
            special = true,
            popups = true,
            vibrancy = 0.18,
            brightness = 1.05,
        },
    },
    group = {
        col = {
            border_active = { colors = { "rgba(AACCDDee)", "rgba(CCB2B9ee)" }, angle = 45 },
            border_inactive = "rgba(DDE6EE66)",
        },
        groupbar = {
            col = {
                active = V.color12,
                inactive = V.color10,
            },
            text_color = V.background,
        },
    },
})
