from libqtile.command.client import InteractiveCommandClient

c = InteractiveCommandClient()

def get_wm_class():
    print(c.group["4"].items())

if __name__ == "__main__": 
    get_wm_class()
