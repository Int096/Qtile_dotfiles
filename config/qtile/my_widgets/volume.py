from libqtile import widget

class MyVolume(widget.Volume):
    def _configure(self, qtile, bar):
        widget.Volume._configure(self, qtile, bar)
        self.volume = self.get_volume()
        if self.volume <= 0:
            self.text = ""
        elif self.volume <= 15:
            self.text = ""
        elif self.volume < 50:
            self.text = ""
        else:
            self.text = ""

    def _update_drawer(self):
        if self.volume <= 0:
            self.text = ""
        elif self.volume <= 15:
            self.text = ""
        elif self.volume < 50:
            self.text = ""
        else:
            self.text = ""
        self.draw()

    def increase_vol(self):
        subprocess.run("amixer -D pipewire sset Master 3%+".split(), capture_output=True)
        self.volume = self.get_volume()

    def decrease_vol(self):
        subprocess.run("amixer -D pipewire sset Master 3%-".split(), capture_output=True)
        self.volume = self.get_volume()

    def mute(self):
        subprocess.run("amixer -c PCH set PCM toggle".split(), capture_output=True)
        self.volume = self.get_volume()

