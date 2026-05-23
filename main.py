import json
import subprocess
import winreg
from pathlib import Path
import typer

app = typer.Typer()
CONFIG_FILE = Path("_configured.json")


def get_python_path() -> str:
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Python\PythonCore",
            0, winreg.KEY_READ
        )
        version = winreg.EnumKey(key, 0)
        install_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            rf"SOFTWARE\Python\PythonCore\{version}\InstallPath",
            0, winreg.KEY_READ
        )
        return winreg.QueryValueEx(install_key, "ExecutablePath")[0]
    except Exception:
        pass

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Python\PythonCore",
            0, winreg.KEY_READ
        )
        version = winreg.EnumKey(key, 0)
        install_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            rf"SOFTWARE\Python\PythonCore\{version}\InstallPath",
            0, winreg.KEY_READ
        )
        return winreg.QueryValueEx(install_key, "ExecutablePath")[0]
    except Exception:
        raise RuntimeError("Python not found")


def add_to_path(folder: str):
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Environment",
        0, winreg.KEY_ALL_ACCESS
    )
    current = winreg.QueryValueEx(key, "PATH")[0]
    if folder not in current:
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, current + ";" + folder)
    winreg.CloseKey(key)


def init_environment():
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps({"configured": False}, indent=4))

    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("configured", False):
        project_path = Path(__file__).resolve().parent
        python_path = get_python_path()

        bat_file = project_path / "clitm.bat"
        bat_file.write_text(
            f'@echo off\n"{python_path}" "{project_path / "main.py"}" %*',
            encoding="utf-8"
        )

        add_to_path(str(project_path))

        data["configured"] = True
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("Setup complete! Restart your terminal and run: clitm")
        raise SystemExit


if __name__ == "__main__":
    from commands import *
    init_environment()
    app()