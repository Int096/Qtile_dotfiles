import os

def set_gtk_theme():
    gnome_schema = "org.gnome.desktop.interface"

    gtk_theme_name    = "Catppuccin-Mocha-Standard-Blue-dark"              
    icon_theme_name   = "Everforest-Light"                  
    cursor_theme_name = "Gruvbox-captaine-white-cursors"    
    font_name         = "'JetBrainsMono Nerd Font Propo 9'"
    
    os.system(f"gsettings set {gnome_schema} gtk-theme {gtk_theme_name}")  
    os.system(f"gsettings set {gnome_schema} icon-theme {icon_theme_name}")
    os.system(f"gsettings set {gnome_schema} cursor-theme {cursor_theme_name}")
    os.system(f"gsettings set {gnome_schema} font-name {font_name}")

if __name__ == "__main__":
    set_gtk_theme()
