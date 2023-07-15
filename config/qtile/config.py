import os
import subprocess

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.popup.toolkit import (
    PopupRelativeLayout,
    PopupImage,
    PopupText
)

from libqtile import bar, hook, layout 
from libqtile.config import Click, Drag, Key, Group, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.backend.wayland import InputConfig
from libqtile.utils import guess_terminal
from libqtile import qtile

from colors import *  
from scripts.set_gtk_theme import set_gtk_rules

def show_power_menu(qtile):
    controls = [
        PopupText(
            background = "#00000000"
        ),
    ]

    layout = PopupRelativeLayout(
        qtile,
        width = 1000,
        height = 200,
        controls = controls,
        background = colors["bg_yellow"],
        initial_focus = None,
    )

    layout.show(centered=True)

#-----------------------------------------------------------
# Для просмотра инфы о классах приложений можно юзать 
# qtile cmd-obj -o cmd -f windows

# Выбор цветовой схемы, цветов
colors = everforest_dark_hard()

#-----------------------------------------------------------
#----------НАСТРОЙКА УСТРОЙСТВ ВВОДА------------------------
#-----------------------------------------------------------

# accel_profile    --
# click_method     -- 
# drag             --
# drag_lock        --
# dwt              --
# left_handed      --
# middle_emulation --
# natural_scroll   --
# pointer_accel    --
# scroll_button    --
# scroll_method    -- Способ скролла
# tap              -- Считать ли "Тап" за нажатие
# tap_button_map   -- "lrm" или "lmr"

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

    "type:keyboard": InputConfig(
    ),
}

#----------------------------------------------------------
#---------ВСЯКИЕ ХУКИ--------------------------------------
#----------------------------------------------------------

# Сделать диалоговые окна плавающими
@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True

# Автостарт приложений
@hook.subscribe.startup_once
def autostart():
        home = os.path.expanduser('~/.config/qtile/autostart.sh')
        subprocess.call([home])

#----------------------------------------------------------
# пло

# Настройки групп ./group.py
groups = [
    Group(name="1", label=""),
    Group(name="2", label=""),
    Group(name="3", label=""),
    Group(name="4", label=""),
    Group(name="8", label="", matches=[Match(wm_class=["evince"])]),
    Group(name="9", label="󱞁", matches=[Match(wm_class=["notion-app"])]),
    Group(name="0", label="", matches=[Match(wm_class=["appimagekit_d2192f48ebc43a9db26e1dfa2bc5097b-Kotatogram_Desktop"])]),
    ]

# Настройки хоткеев ./hotkeys.py
mod = "mod4"
alt = "mod1"
terminal = "kitty"

filemanager = "thunar"
browser = "chromium"

audioLower = "amixer sset Master 3- unmute && amixer sset Headphone unmute && amixer sset Speaker unmute"
audioRaise = "amixer sset Master 3+ unmute && amixer sset Headphone unmute && amixer sset Speaker unmute"
audioMute = "amixer sset Master mute togle"             

brightnessUp = "brightnessctl set +5%"                  
brightnessDown = "brightnessctl set 5%-"                

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

    # Выйти из Qtile
    #Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "e", lazy.function(show_power_menu)),

    # Меню
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Для открытия приложений по клавишам
    Key([mod], "w", lazy.spawn(browser)),
    Key([mod], "m", lazy.spawn(filemanager)),
    Key([mod], "v", lazy.spawn("evince")),
    Key([mod], "d", lazy.spawn("discord")),
    Key([mod], "t", lazy.spawn("kotatogram-desktop")),
    Key([mod], "n", lazy.spawn("notion-app")),
   
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
    
#-----------------------------------------------------------   
#----------------НАСТРОЙКА РАСПОЛОЖЕНИЯ ОКОН----------------
#-----------------------------------------------------------

layouts = [
    layout.Bsp(
        border_focus = colors["blue"],
        border_normal = colors["bg_blue"],
        border_on_single = False, 
        border_width = 2,
        fair = False,
        grow_amount = 5,
        lower_right = True, 
        margin = 2, 
        margin_on_single = 0,
        ratio = 1.4,
        wrap_clitnts = False,
    ),
]

#-----------------------------------------------------------
#----------НАСТРОЙКА БАРА И ВИДЖЕТОВ------------------------
#-----------------------------------------------------------

# Общие параметры виджетов на панели
widget_defaults = dict(
    font     = "JetBrainsMono Nerd Font Propo Bold",
    fontsize = 14,
    padding  = 3,
)
extension_defaults = widget_defaults.copy()

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

# Виджеты на панели
screens = [
    Screen(
        wallpaper = "~/.wallpaper/japanese_pedestrian_street.png",
        wallpaper_mode = "fill",

        top = bar.Bar(
            [
                widget.GroupBox(
                    highlight_method = "text",
                    this_current_screen_border = colors["green"],
                    urgent_alert_method = "text",
                    urgent_text = colors["red"],
                    background = colors["bg5"],
                    active = colors["fg"],
                    inactive = colors["bg2"],
                    fontsize = 22,
                    disable_drag = True,
                    **decoration_group,
                ),
                widget.Prompt(
                    background = colors["bg2"],
                    foreground = colors["fg"],
                    bell_style = None,
                    cursor = False,
                    **decoration_group,
                ),

                widget.Spacer(
                    background = colors["bg2"] + "00",
                    **decoration_group,
                ),

                widget.Clock(
                    format = "󰃭 %d/%m/%y |  %H:%M",
                    background = colors["blue"],
                    foreground = colors["bg2"],
                    **decoration_group,
                ),  
                
                widget.Spacer(
                    background = colors["bg2"] + "00",
                ), 
               
                widget.Wlan(
                    background = colors["orange"],
                    foreground = colors["bg2"],
                    interface = "wlp0s20f3",
                    format = "󰖩 {essid} {percent:2.0%}",
                    **decoration_group,
                ),

                widget.KeyboardLayout(
                    background = colors["yellow"],
                    foreground = colors["bg2"],
                    fmt = "{}",
                    configured_keyboards = ["us", "ru"],                         
                    **decoration_group,
                ),          

                widget.Backlight(
                    background = colors["aqua"],
                    foreground = colors["bg2"],
                    backlight_name = "intel_backlight",
                    fmt = "󰃝 {}",
                    **decoration_group,
                ),

                widget.Battery(
                    background = colors["purple"],
                    foreground = colors["bg2"],
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
                    foreground = colors["bg2"],
                    fmt = "󰕾 {}",
                    **decoration_group,
                ),
            ],
            32,
            background = "#00000000",
            foreground = colors["fg"],
            margin = 5,
            border_width = 0,
        ),
    ),
]

#-----------------------------------------------------------
#-----------------НАСТРОЙКА КОМБИНАЦИЙ С МЫШЬЮ--------------
#-----------------------------------------------------------

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod, "shift"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

# Настройки плавающих окон
floating_layout = layout.Floating(
    border_width = 2,
    border_focus = colors["blue"],
    border_normal = colors["bg_blue"],
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="imv"),
        Match(wm_class="mpv"),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="PowerMenu"),
        Match(wm_class=filemanager),
        Match(wm_class="file-roller"),
        Match(wm_class="com.transmissionbt.transmission_66307_2231745"),        
    ]
)

#-----------------------------------------------------------
#-------ВСЯКИЕ ГЛОБАЛЬНЫЕ НАСТРОЙКИ-------------------------
#-----------------------------------------------------------

auto_fullscreen     = True    # Автоматическое открытие в полноэкранном режиме
bring_front_click   = True    # Вытаскивание приложения на передний край кликом
cursor_warp         = False   # Курсор следует за фокусом
dgroups_key_binder  = None    # Хз
dgroups_app_rules   = []      # Хз
follow_mouse_focus  = True    # Фокус следует за мышью
reconfigure_screens = True    # Что-то про реконфигурировании окон при перечитывании конфига
wmname              = "Qtile"  # Что-то для java-приложений
auto_minimize       = True    # Хз

# Устанавливать фокус на окно, которое этого требует
focus_on_window_activation = "smart"    
