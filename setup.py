import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "forms", "widgets"],
    "includes": ["tkinter", "pystray", "ttkbootstrap", "Pillow", "six"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="copyFile",
    version="1.0",
    description="Faz a copia de um arquivo especifico de tempos em tempos para uma pasta selecionada.",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
