import os     
from libqtile import hook

@hook.subscribe.startup_complete
def set_gtk_rules():
    gnome_schema = "org.gnome.desktop.interface"

    gtk_theme_name    = "Kanagawa-BL"              
    icon_theme_name   = "Everforest-Light"                  
    cursor_theme_name = "Gruvbox-captaine-white-cursors"    
    cursor_size       = "24"
    font_name         = "'JetBrainsMono Nerd Font Propo 9'"
    
    os.system("gsettings set " + gnome_schema + " gtk-theme "    + gtk_theme_name)  
    os.system("gsettings set " + gnome_schema + " icon-theme "   + icon_theme_name)
    os.system("gsettings set " + gnome_schema + " cursor-theme " + cursor_theme_name)
    os.system("gsettings set " + gnome_schema + " font-name "    + font_name)
    os.system("gsettings set " + gnome_schema + " cursor-size "  + cursor_size)
