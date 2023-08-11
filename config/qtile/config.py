from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

from libqtile import  bar, hook, layout 
from libqtile.lazy import lazy
from libqtile.backend.wayland import InputConfig
from libqtile.config import (
    Screen,
    Group,
    Drag,
    Key,
    Match,
)

from my_widgets.battery import MyBattery
from my_widgets.volume import MyVolume



colour_scheme = dict(
    background          = "#313244",
    background_lighter  = "#45475a",
    super_dark_back     = "#1e1e2e",
    foreground          = "#cdd6f4",
    red                 = "#f38ba8",
    green               = "#a6e3a1",
    yellow              = "#f9e2af",
    blue                = "#74c7ec",
    orange              = "#fab387",
    white               = "#bac2de",
    grey                = "#9399b2",
)

# ПОСТАВИТЬ gtk ТЕМУ
from utils.set_gtk_theme import set_gtk_theme
set_gtk_theme()

# АВТОЗАПУСК
@hook.subscribe.startup_once
def autostart():
    import subprocess
    subprocess.Popen(["mako"])

# КЛАВИШИ МОДИФИКАТОРА
mod = "mod4"
alt = "mod1"

# ПРИЛОЖЕНИЯ
terminal_name    = "kitty"
filemanager_name = "thunar"
browser_name     = "chromium"
discord_name     = "discord"
telegram_name    = "kotatogram-desktop"
torrent_name     = "qbittorrent"
notes_name       = "notion-app"
lock_name        = "gtklock"

telegram_class    = "appimagekit_d2192f48ebc43a9db26e1dfa2bc5097b-Kotatogram_Desktop"
torrent_class     = "qbittorrent"
filemanager_class = "thunar"


# ЗВУК И ЯРКОСТЬ
audioLower = "amixer sset Master 3- unmute"
audioRaise = "amixer sset Master 3+ unmute "
audioMute = "amixer sset Master mute togle"             

brightnessUp = "brightnessctl set +5%"                  
brightnessDown = "brightnessctl set 5%-"                


# НАСТРОЙКИ УСТРОЙСТВ ВВОДА 
wl_input_rules = {
    '10182:480:GXTP7863:00 27C6:01E0 Touchpad': InputConfig(
        accel_profile = "adaptive",  
        click_method = "clickfinger",
        drag = True,
        drag_lock = True,
        dwt = True, 
        left_handed = False,
        middle_emulation = True,
        natural_scroll = False,
        pointer_accel = 0.15,
        scroll_button = "disable",
        scroll_method = "two_finger",
        tap = True,
        tap_button_map = "lmr",
    ),
}

# НАСТРОЙКИ ГРУПП 
groups = [
    Group(name="1", label="", layout="bsp"),
    Group(name="2", label="", layout="bsp"),
    Group(name="3", label="", layout="bsp"),
    Group(name="4", label="", layout="bsp"),
    Group(name="7", label="", layout="bsp"),
    Group(name="8", label="󱞁", layout="bsp"),
    Group(name="9", label="󰙯", layout="max"),
    Group(name="0", label="", layout="max"),
    ]

# НАСТРОЙКИ ГОРЯЧИХ КЛАВИШ 
keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window down"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([alt, "shift"], "j", lazy.layout.flip_down()),
    Key([alt, "shift"], "k", lazy.layout.flip_up()),
    Key([alt, "shift"], "h", lazy.layout.flip_left()),
    Key([alt, "shift"], "l", lazy.layout.flip_right()), 
   
    Key([mod, "shift"], "space", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    Key([alt], "h", lazy.screen.prev_group(), desc="Switch to previos group"), 
    Key([alt], "l", lazy.screen.next_group(), desc="Switch to next group"),
    
    Key([], "XF86MonBrightnessUp", lazy.spawn(brightnessUp), desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn(brightnessDown), desc="Decrease breghtness"),
    
    Key([], "XF86AudioLowerVolume", lazy.spawn(audioLower), desc="Increase audio"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(audioRaise), desc="Decrease audio"),
    Key([], "XF86AudioMute", lazy.spawn(audioMute), desc="Mute audio"),
   
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    
    Key([mod, alt], "l", lazy.spawn(lock_name), desc="Screenlock"),
    Key([mod], "Return", lazy.spawn(terminal_name), desc="Launch terminal"),
    Key([mod], "w", lazy.spawn(browser_name), desc="Spawn browser"),
    Key([mod], "m", lazy.spawn(filemanager_name), desc="Spawn file manager"),
    Key([mod], "v", lazy.spawn("evince"), desc="Spawn evince"),
    Key([mod], "d", lazy.spawn(discord_name), desc="Spawn discord"),
    Key([mod], "t", lazy.spawn(telegram_name), desc="Spawn kotatogram"),
    Key([mod], "n", lazy.spawn(notes_name), desc="Spawn notes"),
  
    Key([mod], "Space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard"),
]

for i in groups:
    keys.extend(
        [
            # Переход по группам
            Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),
            
            # Перекидывание по группам
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name)),
        ]
    )
    
from plugins.graphical_notifications import Notifier

notifier = Notifier()

keys.extend([
    Key([mod],          'grave', lazy.function(notifier.prev)),
    Key([mod, 'shift'], 'grave', lazy.function(notifier.next)),
    Key(['control'],    'space', lazy.function(notifier.close)),
])

# НАСТРОЙКИ МАКЕТОВ РАСПОЛОЖЕНИЯ ОКОН 
layout_theme = {
    "border_width"     : 3,
    "margin"           : 4,
    "border_focus"     : colour_scheme["blue"],
    "border_normal"    : colour_scheme["background_lighter"],
    "grow_amount"      : 5,
    "border_on_single" : False,
    "margin_on_single" : False,
}

layouts = [
    layout.Bsp(
        **layout_theme,
        fair = False,
        lower_right = True, 
        ratio = 1.4,
        wrap_clitnts = False,
    ),

    layout.Max(),
]

# ДЕФОЛТНЫЕ НАСТРОЙКИ ВИДЖЕТОВ НА ПАНЕЛИ 
widget_defaults = dict(
    font       = "JetBrainsMono Nerd Font Propo Bold",
    fontsize   = 14,
    padding    = 15,
    background = colour_scheme["background_lighter"],
    foreground = colour_scheme["foreground"],
)
extension_defaults = widget_defaults.copy()

# ПРАВИЛА ДЕКОРАЦИИ ВИДЖЕТОВ НА ПАНЕЛИ


decoration_group = {
    "decorations": [
        RectDecoration(
            colour = colour_scheme["super_dark_back"], 
            radius = 12, 
            filled = True,
            padding = 6,
            group = False,
        ),
    ],
}


# НАСТРОЙКИ ЭКРАНА, БАРА, ВИДЖЕТОВ 
screens = [
    Screen(
        wallpaper = "/home/int/Media/Wallpapers/underwater.png",
        wallpaper_mode = "fill",

        top = bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    foreground = colour_scheme["foreground"],
                    size_percent = 50,
                ),

                widget.GroupBox(
                    borderwidth = 4,
                    active = colour_scheme["blue"],
                    inactive = colour_scheme["grey"],
                    disable_drag = True,
                    rounded = True,
                    highlight_color = colour_scheme["background_lighter"],
                    block_highlight_text_color = colour_scheme["green"],
                    highlight_method = "block",
                    this_current_screen_border = colour_scheme["super_dark_back"],
                    this_screen_border = colour_scheme["orange"],
                    other_current_screen_border = colour_scheme["background_lighter"],
                    other_screen_border = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    background = colour_scheme["background_lighter"],
                    urgent_border = colour_scheme["red"],
                    **decoration_group,
                ),
                
                widget.Sep(
                    linewidth = 0,
                    foreground = colour_scheme["foreground"],
                    padding = 10,
                    size_percent = 50,
                ),
                
                widget.Prompt(
                    background = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    bell_style = None,
                    cursor = False,
                    **decoration_group,
                ),

                widget.Spacer(
                ),

                widget.Clock(
                    format = " %a, %b %d",
                    background = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    **decoration_group,
                ),  
                
                widget.Sep(
                    linewidth = 0,
                    foreground = colour_scheme["background_lighter"],
                    padding = 0,
                    size_percent = 50,
                ),
                
                widget.Clock(
                    format = " %H:%M",
                    background = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    **decoration_group,
                ),  
                
                widget.Spacer(
                ),

                widget.Wlan(
                    background = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    interface = "wlp0s20f3",
                    format = "󰖩 {essid} {percent:2.0%}",
                    disconnected_message = "󰖪",
                    **decoration_group,
                ),

                widget.Sep(
                    linewidth = 0,
                    foreground = colour_scheme["background_lighter"],
                    padding = 0,
                    size_percent = 50,
                ),

                widget.KeyboardLayout(
                    background = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    fmt = "{}",
                    configured_keyboards = ["us", "ru"],                         
                    **decoration_group,
                ),          
                
                widget.Sep(
                    linewidth = 0,
                    foreground = colour_scheme["background_lighter"],
                    padding = 0,
                    size_percent = 50,
                ),

                widget.Backlight(
                    background = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    backlight_name = "intel_backlight",
                    fmt = "󰃝 {}",
                    **decoration_group,
                ),
                
                widget.Sep(
                    linewidth = 0,
                    foreground = colour_scheme["background_lighter"],
                    padding = 0,
                    size_percent = 50,
                ),

                MyBattery(
                    background = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    format = "{char}",
                    low_foreground = colour_scheme["red"],
                    show_short_text = False,
                    **decoration_group,
                ),
                
                widget.Sep(
                    linewidth = 0,
                    foreground = colour_scheme["background_lighter"],
                    padding = 0,
                    size_percent = 50,
                ),

                widget.Volume(
                    background = colour_scheme["background_lighter"],
                    foreground = colour_scheme["foreground"],
                    **decoration_group,
                ),
                
                widget.Sep(
                    linewidth = 0,
                    foreground = colour_scheme["background_lighter"],
                    padding = 10,
                    size_percent = 50,
                ),
            ],
            42,
            margin = 0,
            background = colour_scheme["background_lighter"],
            border_width = [0, 0, 3, 0],
            border_color = colour_scheme["blue"],
        ),
    ),
]

# НАСТРОЙКИ УПРАВЛЕНИЯ МЫШЬЮ
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod, "shift"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

# СДЕЛАТЬ ПЛАВАЮЩИМИ ДИАЛОГОВЫЕ ОКНА
@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True

# НАСТРОЙКИ ПЛАВАЮЩИХ ОКОН 
floating_layout = layout.Floating(
    border_width = 2,
    border_focus = colour_scheme["blue"],
    border_normal = colour_scheme["background_lighter"],

    # Для просмотра инфы о классах приложений можно юзать 
    # qtile cmd-obj -o cmd -f windows

    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        
        Match(wm_class="imv"),
        Match(wm_class="mpv"),
        Match(wm_class=filemanager_class),
        Match(wm_class="file-roller"),
        Match(wm_class=torrent_class),        
    ]
)

# ВСЯКИЕ ГЛОБАЛЬНЫЕ НАСТРОЙКИ
auto_fullscreen     = True    # Автоматическое открытие в полноэкранном режиме
bring_front_click   = True    # Вытаскивание приложения на передний край кликом
cursor_warp         = False   # Курсор следует за фокусом
dgroups_key_binder  = None    # Хз / Тут что-то про динамеческие группы, которые существуют
dgroups_app_rules   = []      # Хз / только при каком-то  условии
follow_mouse_focus  = True    # Фокус следует за мышью
reconfigure_screens = True    # Что-то про реконфигурировании окон при перечитывании конфига
wmname              = "Qtile" # Что-то для java-приложений
auto_minimize       = True    # Хз

# Устанавливать фокус на окно, которое этого требует
focus_on_window_activation = "smart"    
