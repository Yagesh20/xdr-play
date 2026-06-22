import os
import sys
import time
import ctypes
import subprocess
from pathlib import Path

EXE_PATH = r"C:\Users\Mitsuser\Documents\NETSH.exe"
SIMULATION_ARGUMENT = "netsh advfirewall set currentprofile state off"
DETECTION_TYPE = "1"


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0


def relaunch_as_admin():
    script_path = os.path.abspath(__file__)

    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        f'"{script_path}"',
        os.getcwd(),
        1
    )

    sys.exit(0)


def main():
    if not is_admin():
        print("[SIMULATION] Relaunching as Administrator...")
        relaunch_as_admin()

    if not Path(EXE_PATH).exists():
        raise FileNotFoundError(f"Simulation exe not found: {EXE_PATH}")

    full_command = f'"{EXE_PATH}" {SIMULATION_ARGUMENT}'

    cmd_script = (
        'title Hexnode XDR NETSH Threat Simulation && '
        'echo Running Hexnode XDR NETSH Threat Simulation... && '
        f'echo Command: {full_command} && '
        f'{full_command}'
    )

    proc = subprocess.Popen(
        ["cmd.exe", "/k", cmd_script],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    time.sleep(5)

    import pyautogui

    pyautogui.write(DETECTION_TYPE)
    pyautogui.press("enter")

    print("[SIMULATION] Detection type selected.")
    print("[SIMULATION] CMD window is intentionally kept alive.")
    print("[SIMULATION] Do not close it until validation is completed.")


if __name__ == "__main__":
    main()