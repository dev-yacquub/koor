"""
Koor Windows Installer and System Integration Utilities.
Handles automatic PATH registration, .koor file associations, shortcuts, and uninstallation.
All operations target HKEY_CURRENT_USER and %LOCALAPPDATA%, requiring zero admin privileges.
"""

import sys
import os
import subprocess
import shutil

if sys.platform == "win32":
    import winreg
    import ctypes
else:
    winreg = None
    ctypes = None


def get_default_install_dir() -> str:
    """Returns %LOCALAPPDATA%\\Programs\\Koor"""
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        local_app_data = os.path.expanduser(r"~\AppData\Local")
    return os.path.join(local_app_data, "Programs", "Koor")


def notify_windows_environment_change():
    """Broadcasts WM_SETTINGCHANGE so all windows and shells see updated PATH."""
    if sys.platform != "win32" or not ctypes:
        return
    try:
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        res = ctypes.c_long()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            SMTO_ABORTIFHUNG,
            3000,
            ctypes.byref(res)
        )
    except Exception:
        pass


def notify_windows_shell_change():
    """Notifies Windows Explorer of file association changes."""
    if sys.platform != "win32" or not ctypes:
        return
    try:
        SHCNE_ASSOCCHANGED = 0x08000000
        SHCNF_IDLIST = 0
        ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
    except Exception:
        pass


def get_user_path() -> list[str]:
    """Retrieves list of directories in User PATH."""
    if sys.platform != "win32" or not winreg:
        return []
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
            val, _ = winreg.QueryValueEx(key, "Path")
            return [p.strip() for p in val.split(";") if p.strip()]
    except FileNotFoundError:
        return []
    except Exception:
        return []


def is_in_user_path(directory: str) -> bool:
    """Checks if directory is currently in User PATH."""
    norm_target = os.path.normcase(os.path.abspath(directory))
    for p in get_user_path():
        if os.path.normcase(os.path.abspath(p)) == norm_target:
            return True
    return False


def add_to_user_path(directory: str) -> bool:
    """
    Appends directory to User PATH in HKCU\\Environment if not already present.
    Returns True if added, False if already existed.
    """
    if sys.platform != "win32" or not winreg:
        return False

    norm_target = os.path.normcase(os.path.abspath(directory))
    paths = get_user_path()

    for p in paths:
        if os.path.normcase(os.path.abspath(p)) == norm_target:
            return False  # Already present

    # Add target directory to paths
    paths.append(os.path.abspath(directory))
    new_path_str = ";".join(paths) + ";"

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path_str)

    # Also update current process environment
    current_os_path = os.environ.get("Path", "")
    if norm_target not in [os.path.normcase(os.path.abspath(x)) for x in current_os_path.split(";") if x]:
        os.environ["Path"] = f"{os.path.abspath(directory)};{current_os_path}"

    notify_windows_environment_change()
    return True


def remove_from_user_path(directory: str) -> bool:
    """Removes directory from User PATH in HKCU\\Environment."""
    if sys.platform != "win32" or not winreg:
        return False

    norm_target = os.path.normcase(os.path.abspath(directory))
    paths = get_user_path()
    filtered = [p for p in paths if os.path.normcase(os.path.abspath(p)) != norm_target]

    if len(filtered) == len(paths):
        return False

    new_path_str = ";".join(filtered) + (";" if filtered else "")

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path_str)

    notify_windows_environment_change()
    return True


def register_file_association(exe_path: str) -> bool:
    """
    Registers .koor file association in HKCU\\Software\\Classes:
    - Double click -> koor.exe run "%1"
    - Right-click menu -> 'Ku wad Koor (Run with Koor)'
    """
    if sys.platform != "win32" or not winreg:
        return False

    try:
        abs_exe = os.path.abspath(exe_path)

        # 1. Register extension
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.koor") as ext_key:
            winreg.SetValueEx(ext_key, "", 0, winreg.REG_SZ, "KoorSourceFile")

        # 2. Register ProgID
        prog_id = r"Software\Classes\KoorSourceFile"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, prog_id) as prog_key:
            winreg.SetValueEx(prog_key, "", 0, winreg.REG_SZ, "Koor Source File (.koor)")

        # 3. Default Icon
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{prog_id}\\DefaultIcon") as icon_key:
            winreg.SetValueEx(icon_key, "", 0, winreg.REG_SZ, f'"{abs_exe}",0')

        # 4. Open command
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{prog_id}\\shell\\open\\command") as cmd_key:
            winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, f'"{abs_exe}" run "%1"')

        # 5. Custom context menu command
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{prog_id}\\shell\\run_koor") as run_menu_key:
            winreg.SetValueEx(run_menu_key, "", 0, winreg.REG_SZ, "Ku wad Koor (Run with Koor)")

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{prog_id}\\shell\\run_koor\\command") as run_cmd_key:
            winreg.SetValueEx(run_cmd_key, "", 0, winreg.REG_SZ, f'"{abs_exe}" run "%1"')

        notify_windows_shell_change()
        return True
    except Exception as e:
        print(f"Warning: Could not register file association: {e}")
        return False


def unregister_file_association() -> bool:
    """Removes .koor file association keys from HKCU\\Software\\Classes."""
    if sys.platform != "win32" or not winreg:
        return False

    def delete_key_tree(root, subkey):
        try:
            with winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS) as k:
                while True:
                    try:
                        child = winreg.EnumKey(k, 0)
                        delete_key_tree(root, f"{subkey}\\{child}")
                    except OSError:
                        break
            winreg.DeleteKey(root, subkey)
        except FileNotFoundError:
            pass
        except Exception:
            pass

    delete_key_tree(winreg.HKEY_CURRENT_USER, r"Software\Classes\.koor")
    delete_key_tree(winreg.HKEY_CURRENT_USER, r"Software\Classes\KoorSourceFile")
    notify_windows_shell_change()
    return True


def create_shortcuts(exe_path: str, desktop: bool = True) -> list[str]:
    """Creates Start Menu and optional Desktop shortcuts using WScript.Shell."""
    if sys.platform != "win32":
        return []

    abs_exe = os.path.abspath(exe_path)
    exe_dir = os.path.dirname(abs_exe)
    created = []

    # Start menu folder
    appdata = os.environ.get("APPDATA", os.path.expanduser(r"~\AppData\Roaming"))
    start_menu_dir = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Koor")
    os.makedirs(start_menu_dir, exist_ok=True)
    start_lnk = os.path.join(start_menu_dir, "Koor REPL.lnk")

    powershell_lines = [
        f'$ws = New-Object -ComObject WScript.Shell;',
        f'$s = $ws.CreateShortcut("{start_lnk}");',
        f'$s.TargetPath = "{abs_exe}";',
        f'$s.Arguments = "repl";',
        f'$s.WorkingDirectory = "{exe_dir}";',
        f'$s.Description = "Koor Programming Language REPL";',
        f'$s.Save();'
    ]

    if desktop:
        userprofile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        desktop_dir = os.path.join(userprofile, "Desktop")
        if os.path.exists(desktop_dir):
            desktop_lnk = os.path.join(desktop_dir, "Koor REPL.lnk")
            powershell_lines.extend([
                f'$s2 = $ws.CreateShortcut("{desktop_lnk}");',
                f'$s2.TargetPath = "{abs_exe}";',
                f'$s2.Arguments = "repl";',
                f'$s2.WorkingDirectory = "{exe_dir}";',
                f'$s2.Description = "Koor Programming Language REPL";',
                f'$s2.Save();'
            ])
            created.append(desktop_lnk)

    created.append(start_lnk)

    ps_script = " ".join(powershell_lines)
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
    except Exception:
        pass

    return created


def remove_shortcuts():
    """Removes Koor Start Menu and Desktop shortcuts."""
    if sys.platform != "win32":
        return

    appdata = os.environ.get("APPDATA", os.path.expanduser(r"~\AppData\Roaming"))
    start_menu_dir = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Koor")
    if os.path.exists(start_menu_dir):
        shutil.rmtree(start_menu_dir, ignore_errors=True)

    userprofile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    desktop_lnk = os.path.join(userprofile, "Desktop", "Koor REPL.lnk")
    if os.path.exists(desktop_lnk):
        try:
            os.remove(desktop_lnk)
        except Exception:
            pass


def register_windows_uninstall(install_dir: str, exe_path: str, version: str = "1.0.0") -> bool:
    """Registers Koor in Windows Add/Remove Programs (Installed Apps)."""
    if sys.platform != "win32" or not winreg:
        return False

    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Koor"
        abs_exe = os.path.abspath(exe_path)
        abs_dir = os.path.abspath(install_dir)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as k:
            winreg.SetValueEx(k, "DisplayName", 0, winreg.REG_SZ, "Koor Programming Language")
            winreg.SetValueEx(k, "DisplayVersion", 0, winreg.REG_SZ, version)
            winreg.SetValueEx(k, "Publisher", 0, winreg.REG_SZ, "Koor Core Team")
            winreg.SetValueEx(k, "InstallLocation", 0, winreg.REG_SZ, abs_dir)
            winreg.SetValueEx(k, "DisplayIcon", 0, winreg.REG_SZ, f'"{abs_exe}",0')
            winreg.SetValueEx(k, "UninstallString", 0, winreg.REG_SZ, f'"{abs_exe}" uninstall')
            winreg.SetValueEx(k, "NoModify", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(k, "NoRepair", 0, winreg.REG_DWORD, 1)
        return True
    except Exception:
        return False


def unregister_windows_uninstall() -> bool:
    """Removes Koor entry from Windows Add/Remove Programs."""
    if sys.platform != "win32" or not winreg:
        return False
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Koor")
        return True
    except Exception:
        return False
