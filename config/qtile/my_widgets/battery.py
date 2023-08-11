from libqtile.widget.battery import Battery, BatteryState

class MyBattery(Battery):
    """
    """
    
    press_flag = False

    def build_string(self, status):
        if self.layout is not None:
            self.layout.colour = self.foreground
            if (
                status.state == BatteryState.DISCHARGING
                and status.percent < self.low_percentage
            ):
                self.layout.colour = self.low_foreground
                self.background = self.low_background
            else:
                self.layout.colour = self.foreground
                self.background = self.normal_background

        if status.state == BatteryState.DISCHARGING:
            if status.percent > 0.90:
                char = "󰂂"
            elif status.percent > 0.80:
                char = "󰂁"
            elif status.percent > 0.70:
                char = "󰂀"
            elif status.percent > 0.60:
                char = "󰁿"
            elif status.percent > 0.50:
                char = "󰁾"
            elif status.percent > 0.40:
                char = "󰁽"
            elif status.percent > 0.30:
                char = "󰁼"
            elif status.percent > 0.20:
                char = "󰁻"
            elif status.percent > 0.10:
                char = "󰁺"
            else:
                char = "󰂎"
        elif status.percent >= 1 or status.state == BatteryState.FULL:
            char = "󰁹"
        elif status.state == BatteryState.EMPTY or (
            status.state == BatteryState.UNKNOWN and status.percent == 0
        ):
            char = "󰂎"
        else:
            char = "󰂄"
        return self.format.format(char=char, percent=status.percent)
  
    def restore(self):
        self.format = "{char}"
        self.timer_setup()

    def button_press(self, x, y, button):
        self.format = "{char} {percent:2.0%}"
        self.timer_setup()
        self.timeout_add(1, self.restore)
