# setup.py
from cx_Freeze import setup, Executable

setup(
    name="MyApp",
    version="1.0",
    description="My Raspberry Pi GUI App",
    executables=[Executable("NewUI.py", base="GUI")]
)
