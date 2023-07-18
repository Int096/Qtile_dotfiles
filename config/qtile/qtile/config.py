import os
import subprocess

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

from libqtile import bar, hook, layout 
from libqtile.config import Click, Drag, Key, Group, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.backend.wayland import InputConfig
from libqtile import qtile

from colors import *  
from utils.set_gtk_theme import set_gtk_rules

#-----------------------------------------------------------
# АВТОЗАПУСК
@hook.subscribe.startup_once
def autostart():
        home = os.path.expanduser('~/.config/qtile/autostart.sh')
        subprocess.call([home])

# ЦВЕТОВАЯ СХЕМА  
colors = kanagawa()

# КЛАВИШИ МОДИФИКАТОРА
mod = "mod4"
alt = "mod1"

# ПРИЛОЖЕНИЯ
terminal = "kitty"
filemanager = "thunar"
browser = "chromium"

# ЗВУК И ЯРКОСТЬ
audioLower = "amixer sset Master 3- unmute && amixer sset Headphone unmute && amixer sset Speaker unmute"
audioRaise = "amixer sset Master 3+ unmute && amixer sset Headphone unmute && amixer sset Speaker unmute"
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
        tap_button_map = "lrm",
    ),
}

# НАСТРОЙКИ ГРУПП 
groups = [
    Group(name="1", label="", layout="bsp"),
    Group(name="2", label="", layout="bsp"),
    Group(name="3", label="", layout="bsp"),
    Group(name="4", label="", layout="monadtall"),
    Group(name="7", label="", layout="columns", matches=[Match(wm_class=["evince"])]),
    Group(name="8", label="󱞁", layout="bsp", matches=[Match(wm_class=["obsidian"])]),
    Group(name="9", label="󰙯", layout="max", matches=[Match(wm_class=["discord"])]),
    Group(name="0", label="", layout="max", matches=[Match(wm_class=["appimagekit_d2192f48ebc43a9db26e1dfa2bc5097b-Kotatogram_Desktop"])]),
    ]

# НАСТРОЙКИ ГОРЯЧИХ КЛАВИШ 
keys = [
    # Передвижение окон
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    
    # Перекидывание окон
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Ресайз окон
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # ----
    Key([alt, "shift"], "j", lazy.layout.flip_down()),
    Key([alt, "shift"], "k", lazy.layout.flip_up()),
    Key([alt, "shift"], "h", lazy.layout.flip_left()),
    Key([alt, "shift"], "l", lazy.layout.flip_right()), 
   
    # Смена split на unsplit и обратно, нужно для stack и columns
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Перейти на предыдущую группу
    Key([alt], "h", lazy.screen.prev_group(), desc="Switch to previos group"), 

    # Перейти на следующую группу
    Key([alt], "l", lazy.screen.next_group(), desc="Switch to next group"),
    
    # Регулировка яркости кнопками
    Key([], "XF86MonBrightnessUp", lazy.spawn(brightnessUp), desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn(brightnessDown), desc="Decrease breghtness"),
    
    # Регулировка звука
    Key([], "XF86AudioLowerVolume", lazy.spawn(audioLower), desc="Increase audio"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(audioRaise), desc="Decrease audio"),
    Key([], "XF86AudioMute", lazy.spawn(audioMute), desc="Mute audio"),
   
    # Развернуть окно в полный экран
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    
    # Сделать окно плавающим и обратно
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),

    # Открыть терминал
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    
    # Убить окно
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    
    # Перечитать конфиг
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),

    # Убить Qtile 
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),

    # Prompt Меню
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Для открытия приложений по клавишам
    Key([mod], "w", lazy.spawn(browser), desc="Spawn browser"),
    Key([mod], "m", lazy.spawn(filemanager), desc="Spawn file manager"),
    Key([mod], "v", lazy.spawn("evince"), desc="Spawn evince"),
    Key([mod], "d", lazy.spawn("discord"), desc="Spawn discord"),
    Key([mod], "t", lazy.spawn("kotatogram-desktop -platform wayland"), desc="Spawn kotatogram"),
    Key([mod], "n", lazy.spawn("obsidian"), desc="Spawn obsidian"),
   
    # Смена раскладки
    Key([mod], "Space", lazy.widget["keyboardlayout"].next_keyboard()),
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
    
# НАСТРОЙКИ МАКЕТОВ РАСПОЛОЖЕНИЯ ОКОН 
layouts = [
    layout.Bsp(
        border_focus = colors["blue"],
        border_normal = colors["bg_blue"],
        border_on_single = False, 
        border_width = 2,
        fair = False,
        grow_amount = 5,
        lower_right = True, 
        margin = 3, 
        margin_on_single = (5, 0, 0, 0),
        ratio = 1.4,
        wrap_clitnts = False,
    ),

    layout.MonadTall(
        border_focus = colors["blue"],
        border_normal = colors["bg_blue"],
        margin = 3,
    ),

    layout.Columns(
        border_focus = colors["blue"],
        border_normal = colors["bg_blue"],
        border_focus_stack = colors["blue"],
        border_normal_stack = colors["bg_blue"],
        margin = 3,
        num_columns = 3,
    ),

    layout.Max(),
]

# ДЕФОЛТНЫЕ НАСТРОЙКИ ВИДЖЕТОВ НА ПАНЕЛИ 
widget_defaults = dict(
    font     = "JetBrainsMono Nerd Font Propo Bold",
    fontsize = 14,
    padding  = 3,
)
extension_defaults = widget_defaults.copy()

# ПРАВИЛА ДЕКОРАЦИИ ВИДЖЕТОВ НА ПАНЕЛИ
decoration_group = {
    "decorations": [
        RectDecoration(
            colour = "#00000000", 
            radius = 15, 
            filled = True, 
            padding_y = 2, 
            group = False,
            use_widget_background = True,
        )
    ],
    "padding": 10,
}

# НАСТРОЙКИ ЭКРАНА, БАРА, ВИДЖЕТОВ 
screens = [
    Screen(
        wallpaper = "~/.wallpaper/wallpap.jpg",
        wallpaper_mode = "fill",

        top = bar.Bar(
            [
                widget.GroupBox(
                    highlight_method = "text",
                    this_current_screen_border = colors["green"],
                    urgent_alert_method = "text",
                    urgent_text = colors["red"],
                    background = colors["bg_gray"],
                    active = colors["fg"],
                    inactive = colors["bg_dark"],
                    fontsize = 16,
                    disable_drag = True,
                    **decoration_group,
                ),
                widget.Prompt(
                    background = colors["bg_dark"],
                    foreground = colors["fg"],
                    bell_style = None,
                    cursor = False,
                    **decoration_group,
                ),

                widget.Spacer(
                    background = colors["bg_dark"] + "00",
                    **decoration_group,
                ),

                widget.Clock(
                    format = "󰃭 %d/%m/%y |  %H:%M",
                    background = colors["blue"],
                    foreground = colors["bg_dark"],
                    **decoration_group,
                ),  
                
                widget.Spacer(
                    background = colors["bg_dark"] + "00",
                ),

                widget.TextBox(
                    text = " ",
                ),
               
                widget.Wlan(
                    background = colors["orange"],
                    foreground = colors["bg_dark"],
                    interface = "wlp0s20f3",
                    format = "󰖩 {essid} {percent:2.0%}",
                    disconnected_message = "󰖪",
                    **decoration_group,
                ),

                widget.TextBox(
                    text = " ",
                ),

                widget.KeyboardLayout(
                    background = colors["yellow"],
                    foreground = colors["bg_dark"],
                    fmt = "{}",
                    configured_keyboards = ["us", "ru"],                         
                    **decoration_group,
                ),          

                widget.TextBox(
                    text = " ",
                ),

                widget.Backlight(
                    background = colors["aqua"],
                    foreground = colors["bg_dark"],
                    backlight_name = "intel_backlight",
                    fmt = "󰃝 {}",
                    **decoration_group,
                ),
                
                widget.Battery(
                    background = colors["purple"],
                    foreground = colors["bg_dark"],
                    format = "{char} {percent:2.0%}",
                    update_interval = 5,
                    full_char = "󰁹",
                    charge_char = "󱟦",
                    discharge_char = "󱟤",
                    empty_char = "󰂃",
                    **decoration_group,
                ),
                
                widget.Volume(
                    background = colors["red"],
                    foreground = colors["bg_dark"],
                    fmt = "󰕾 {}",
                    **decoration_group,
                ),
            ],
            32,
            background = colors["bg_gray"] + "00",
            foreground = colors["fg"],
            margin = (5, 25, 0, 25), 
            border_width = 0,
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
    border_focus = colors["blue"],
    border_normal = colors["bg_blue"],


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
        Match(wm_class=filemanager),
        Match(wm_class="file-roller"),
        Match(wm_class="com.transmissionbt.transmission_66307_2231745"),        
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
