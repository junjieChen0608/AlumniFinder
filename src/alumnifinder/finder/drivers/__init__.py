import os

dir = os.path.dirname(__file__)

# ALL CHROMEDRIVER VERSIONS: 2.31
LINUX_DRIVER_PATH = os.path.join(dir, "chromedriver_linux64")
MAC_DRIVER_PATH = os.path.join(dir, "chromedriver_mac64")
WIN_DRIVER_PATH = os.path.join(dir, "chromedriver_win32.exe")
