"""
Koor Windows Standalone Setup Wizard (KoorSetup).
Provides a one-click graphical installer that requires zero admin permissions.
Installs to %LocalAppData%\\Programs\\Koor, automatically configures User PATH,
registers .koor file associations, and creates desktop/start shortcuts.
"""

import sys
import os
import io
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def safe_print(msg: str):
    if sys.stdout is None:
        return
    try:
        sys.stdout.write(f"{msg}\n")
        sys.stdout.flush()
    except Exception:
        try:
            clean = str(msg).encode('ascii', errors='replace').decode('ascii')
            sys.stdout.write(f"{clean}\n")
            sys.stdout.flush()
        except Exception:
            pass

if sys.platform == "win32":
    try:
        if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if sys.stderr is not None and hasattr(sys.stderr, 'buffer'):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Import installation utilities from koor
try:
    from koor.installer_utils import (
        get_default_install_dir,
        add_to_user_path,
        register_file_association,
        create_shortcuts,
        register_windows_uninstall,
        notify_windows_environment_change,
        notify_windows_shell_change,
    )
except ImportError:
    # Fallback if running standalone
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from koor.installer_utils import (
        get_default_install_dir,
        add_to_user_path,
        register_file_association,
        create_shortcuts,
        register_windows_uninstall,
        notify_windows_environment_change,
        notify_windows_shell_change,
    )

VERSION = "1.0.0"


def get_bundled_file(filename: str) -> str:
    """Locates bundled files either in PyInstaller _MEIPASS or current directory."""
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, filename)
        if os.path.exists(path):
            return path

    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, filename),
        os.path.join(base_dir, "dist", filename),
        os.path.join(base_dir, "..", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return ""


def perform_install(target_dir: str, add_path: bool, assoc_files: bool, context_menu: bool, shortcuts: bool, log_callback=None):
    """Executes the full installation procedure."""
    def log(msg):
        if log_callback:
            log_callback(msg)

    log(f"Abuuraya galka: {target_dir}")
    os.makedirs(target_dir, exist_ok=True)
    examples_dir = os.path.join(target_dir, "examples")
    os.makedirs(examples_dir, exist_ok=True)

    # 1. Copy koor.exe
    log("Koobiyeynaya Koor binary (koor.exe)...")
    src_exe = get_bundled_file("koor.exe")
    dest_exe = os.path.join(target_dir, "koor.exe")

    if src_exe and os.path.exists(src_exe):
        shutil.copy2(src_exe, dest_exe)
    else:
        # Check current python environment koor script or exe
        curr_exe = sys.executable
        log("Fiiro gaar ah: Isticmaalaya nooca binary-ga ee hadda jira...")
        if os.path.exists("koor.exe"):
            shutil.copy2("koor.exe", dest_exe)

    # 2. Copy documentation and book if available
    src_book = get_bundled_file("THE_KOOR_BOOK.pdf")
    if src_book and os.path.exists(src_book):
        log("Koobiyeynaya Buugga Koor (PDF)...")
        shutil.copy2(src_book, os.path.join(target_dir, "THE_KOOR_BOOK.pdf"))

    # 3. Create example scripts
    tusaale_path = os.path.join(examples_dir, "tusaale.koor")
    with open(tusaale_path, "w", encoding="utf-8") as f:
        f.write('''# Tusaale Koor - Ku soo dhawoow dunida Koor!
soo saar "========================================"
soo saar "🇸🇴 Ku soo dhawoow Luuqadda Koor!"
soo saar "========================================"

x waa 15 ku dar 10
soo saar "15 ku dar 10 = {x}"

hawl
magaceed waa : labanlaab
tibxuhu waa : n
hawshu waa : n ku dhufo 2
kaydi natiijada

jawaab waa qabo hawshan (labanlaab) (25)
soo saar "Labanlaabka 25 waa: {jawaab}"
''')

    # 4. Create uninstall.bat helper
    uninst_path = os.path.join(target_dir, "uninstall.bat")
    with open(uninst_path, "w", encoding="utf-8") as f:
        f.write(f'''@echo off
title Ka saaridda Koor
echo Ka saaraya Koor nidaamka Windows...
"{dest_exe}" uninstall
echo Koor si guul leh ayaa looga saaray nidaamka.
pause
''')

    # 5. Add to PATH
    if add_path:
        log("Ku daraya User PATH nidaamka...")
        add_to_user_path(target_dir)

    # 6. File Association
    if assoc_files:
        log("Xiriirinaya faylasha .koor...")
        register_file_association(dest_exe)

    # 7. Create Shortcuts
    if shortcuts:
        log("Abuuraya toobiyaha Start Menu & Desktop...")
        create_shortcuts(dest_exe, desktop=True)

    # 8. Register Windows Uninstall entry
    log("Diiwaangelinaya Koor Settings-ka Windows...")
    register_windows_uninstall(target_dir, dest_exe, VERSION)

    # 9. Notify environment
    log("Cusboonaysiinaya nidaamka Windows...")
    notify_windows_environment_change()
    notify_windows_shell_change()

    log("✅ Rakibaadda Koor si buuxda ayay u dhammaatay!")
    return dest_exe


class KoorInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Koor Programming Language - Setup")
        self.root.geometry("620x540")
        self.root.minsize(580, 500)
        self.root.configure(bg="#0f172a")

        # Set icon if available
        ico = get_bundled_file("koor.ico")
        if ico and os.path.exists(ico):
            try:
                self.root.iconbitmap(ico)
            except Exception:
                pass

        self.target_dir = tk.StringVar(value=get_default_install_dir())
        self.chk_path = tk.BooleanVar(value=True)
        self.chk_assoc = tk.BooleanVar(value=True)
        self.chk_context = tk.BooleanVar(value=True)
        self.chk_shortcuts = tk.BooleanVar(value=True)
        self.installed_exe = None

        self.setup_ui()

    def setup_ui(self):
        # Header banner
        header = tk.Frame(self.root, bg="#1e293b", height=85)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title_lbl = tk.Label(
            header,
            text="🇸🇴  KOOR PROGRAMMING LANGUAGE",
            font=("Segoe UI", 15, "bold"),
            fg="#38bdf8",
            bg="#1e293b"
        )
        title_lbl.pack(anchor="w", padx=24, pady=(16, 2))

        sub_lbl = tk.Label(
            header,
            text="The Natural Somali Language Environment for Windows • Official Setup",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        sub_lbl.pack(anchor="w", padx=24)

        # Main content card
        self.content_frame = tk.Frame(self.root, bg="#0f172a")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)

        self.show_welcome_page()

    def show_welcome_page(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        intro_text = (
            "Ku soo dhawoow rakibaadda Luuqadda Koor! Saaxaddani waxay si toos ah "
            "Koor ugu dari doontaa nidaamkaaga adigoon u baahnayn maamulaha (Admin) ama "
            "habayn gacanta ah oo PATH ah. Marka ay dhamaato, waad isticmaali kartaa isla markiiba."
        )
        desc_lbl = tk.Label(
            self.content_frame,
            text=intro_text,
            font=("Segoe UI", 9),
            fg="#e2e8f0",
            bg="#0f172a",
            wraplength=560,
            justify="left"
        )
        desc_lbl.pack(anchor="w", pady=(0, 14))

        # Destination Folder Frame
        dest_card = tk.LabelFrame(
            self.content_frame,
            text=" Galka Lagu Rakibayo (Installation Folder) ",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg="#1e293b",
            padx=12,
            pady=10
        )
        dest_card.pack(fill=tk.X, pady=(0, 14))

        dir_entry = tk.Entry(
            dest_card,
            textvariable=self.target_dir,
            font=("Segoe UI", 9),
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#475569",
            highlightcolor="#38bdf8"
        )
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 8))

        browse_btn = tk.Button(
            dest_card,
            text="Dooro...",
            font=("Segoe UI", 9),
            bg="#334155",
            fg="#f8fafc",
            activebackground="#475569",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            cursor="hand2",
            command=self.browse_dir
        )
        browse_btn.pack(side=tk.RIGHT)

        # Options Frame
        opts_card = tk.LabelFrame(
            self.content_frame,
            text=" Habaynta Tooska ah (Automatic Configuration) ",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg="#1e293b",
            padx=14,
            pady=10
        )
        opts_card.pack(fill=tk.X, pady=(0, 16))

        c1 = tk.Checkbutton(
            opts_card,
            text="Ku dar User PATH (Ka fur 'koor' terminal kasta adigoon jid qorin)",
            variable=self.chk_path,
            font=("Segoe UI", 9, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
            activebackground="#1e293b",
            activeforeground="#38bdf8",
            selectcolor="#0f172a"
        )
        c1.pack(anchor="w", pady=2)

        c2 = tk.Checkbutton(
            opts_card,
            text="Xiriiri faylasha .koor (Laba-guji si aad toos ugu fuliso barnaamijyada)",
            variable=self.chk_assoc,
            font=("Segoe UI", 9),
            fg="#f8fafc",
            bg="#1e293b",
            activebackground="#1e293b",
            activeforeground="#38bdf8",
            selectcolor="#0f172a"
        )
        c2.pack(anchor="w", pady=2)

        c3 = tk.Checkbutton(
            opts_card,
            text="Ku dar Menu-ga Midig (Right-Click context menu 'Ku wad Koor')",
            variable=self.chk_context,
            font=("Segoe UI", 9),
            fg="#f8fafc",
            bg="#1e293b",
            activebackground="#1e293b",
            activeforeground="#38bdf8",
            selectcolor="#0f172a"
        )
        c3.pack(anchor="w", pady=2)

        c4 = tk.Checkbutton(
            opts_card,
            text="Samee toobiyaha Start Menu & Desktop (Shortcuts)",
            variable=self.chk_shortcuts,
            font=("Segoe UI", 9),
            fg="#f8fafc",
            bg="#1e293b",
            activebackground="#1e293b",
            activeforeground="#38bdf8",
            selectcolor="#0f172a"
        )
        c4.pack(anchor="w", pady=2)

        # Bottom Action Bar
        btn_bar = tk.Frame(self.content_frame, bg="#0f172a")
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=6)

        cancel_btn = tk.Button(
            btn_bar,
            text="Ka Noqo (Cancel)",
            font=("Segoe UI", 9),
            bg="#334155",
            fg="#cbd5e1",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.root.quit
        )
        cancel_btn.pack(side=tk.LEFT)

        self.install_btn = tk.Button(
            btn_bar,
            text="  🚀 RAKIB KOOR (INSTALL NOW)  ",
            font=("Segoe UI", 10, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=6,
            cursor="hand2",
            command=self.start_installation
        )
        self.install_btn.pack(side=tk.RIGHT)

    def browse_dir(self):
        d = filedialog.askdirectory(initialdir=self.target_dir.get(), title="Dooro galka rakibaadda")
        if d:
            self.target_dir.set(os.path.normpath(d))

    def start_installation(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        prog_title = tk.Label(
            self.content_frame,
            text="Rakibaya Koor nidaamkaaga...",
            font=("Segoe UI", 11, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        )
        prog_title.pack(anchor="w", pady=(10, 8))

        self.prog_bar = ttk.Progressbar(self.content_frame, mode="indeterminate", length=540)
        self.prog_bar.pack(fill=tk.X, pady=(0, 14))
        self.prog_bar.start(10)

        # Log box
        self.log_box = tk.Text(
            self.content_frame,
            font=("Consolas", 8),
            bg="#020617",
            fg="#38bdf8",
            relief=tk.FLAT,
            height=12,
            padx=8,
            pady=8
        )
        self.log_box.pack(fill=tk.BOTH, expand=True)

        # Worker thread
        t = threading.Thread(target=self._run_install_thread, daemon=True)
        t.start()

    def _run_install_thread(self):
        try:
            target = self.target_dir.get()
            exe = perform_install(
                target_dir=target,
                add_path=self.chk_path.get(),
                assoc_files=self.chk_assoc.get(),
                context_menu=self.chk_context.get(),
                shortcuts=self.chk_shortcuts.get(),
                log_callback=self._log_msg
            )
            self.installed_exe = exe
            self.root.after(800, self.show_success_page)
        except Exception as e:
            self.root.after(100, lambda: messagebox.showerror("Khalad", f"Rakibaaddu ma guulaysan:\n{e}"))

    def _log_msg(self, msg: str):
        def _append():
            self.log_box.insert(tk.END, f"{msg}\n")
            self.log_box.see(tk.END)
        self.root.after(0, _append)

    def show_success_page(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        succ_frame = tk.Frame(self.content_frame, bg="#0f172a")
        succ_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        check_lbl = tk.Label(
            succ_frame,
            text="🎉",
            font=("Segoe UI", 42),
            bg="#0f172a",
            fg="#10b981"
        )
        check_lbl.pack(pady=(0, 4))

        title_lbl = tk.Label(
            succ_frame,
            text="HAMBALYO! RAKIBAADDU WAY DHAMMAATAY!",
            font=("Segoe UI", 13, "bold"),
            fg="#10b981",
            bg="#0f172a"
        )
        title_lbl.pack(pady=(0, 8))

        detail_text = (
            "Luuqadda Koor si buuxda ayaa loogu daray nidaamkaaga Windows!\n\n"
            "✨ WAXA AAD HADDABA SAMEYN KARTAA:\n"
            "1. Fur terminal kasta (PowerShell ama CMD) oo toos u qor: 'koor'\n"
            "2. Fuli fayl kasta: 'koor run magaca_faylka.koor'\n"
            "3. Laba-guji (Double-click) fayl kasta oo .koor ah si uu toos ugu shaqeeyo\n"
            "4. Fur barnaamijka tooska ah ee 'Koor REPL' ee Start Menu ama Desktop-kaaga"
        )
        detail_lbl = tk.Label(
            succ_frame,
            text=detail_text,
            font=("Segoe UI", 9),
            fg="#e2e8f0",
            bg="#1e293b",
            padx=16,
            pady=12,
            justify="left",
            wraplength=540,
            relief=tk.FLAT
        )
        detail_lbl.pack(fill=tk.X, pady=(0, 16))

        # Action Buttons
        act_bar = tk.Frame(succ_frame, bg="#0f172a")
        act_bar.pack(fill=tk.X, pady=6)

        repl_btn = tk.Button(
            act_bar,
            text="  ⚡ FUR KOOR REPL HADDA  ",
            font=("Segoe UI", 9, "bold"),
            bg="#10b981",
            fg="#ffffff",
            activebackground="#059669",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.launch_repl
        )
        repl_btn.pack(side=tk.LEFT, padx=(0, 8))

        book_btn = tk.Button(
            act_bar,
            text="📖 Fur Buugga (PDF)",
            font=("Segoe UI", 9),
            bg="#334155",
            fg="#f8fafc",
            activebackground="#475569",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.open_book
        )
        book_btn.pack(side=tk.LEFT, padx=(0, 8))

        close_btn = tk.Button(
            act_bar,
            text="Dhammee (Close)",
            font=("Segoe UI", 9),
            bg="#1e293b",
            fg="#cbd5e1",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.root.quit
        )
        close_btn.pack(side=tk.RIGHT)

    def launch_repl(self):
        target = self.target_dir.get()
        exe = os.path.join(target, "koor.exe")
        if os.path.exists(exe):
            cmd = f'start "Koor REPL" cmd /k ""{exe}" repl"'
            subprocess.Popen(cmd, shell=True)
            self.root.quit()
        else:
            messagebox.showinfo("Fiiro gaar ah", "Fur PowerShell ama CMD oo qor 'koor'.")

    def open_book(self):
        target = self.target_dir.get()
        pdf = os.path.join(target, "THE_KOOR_BOOK.pdf")
        if os.path.exists(pdf):
            os.startfile(pdf)
        else:
            messagebox.showinfo("Buugga", "Buuggu wuxuu ku yaallaa galka Koor.")


def run_silent():
    """Silent unattended installation for CLI/Scripts."""
    target = get_default_install_dir()
    perform_install(
        target_dir=target,
        add_path=True,
        assoc_files=True,
        context_menu=True,
        shortcuts=True,
        log_callback=safe_print
    )
    safe_print("✅ Koor silent installation complete.")


def main():
    if "--silent" in sys.argv or "/silent" in sys.argv or "/S" in sys.argv or "-s" in sys.argv:
        run_silent()
        return

    root = tk.Tk()
    # Configure ttk styling
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Horizontal.TProgressbar", troughcolor="#1e293b", background="#38bdf8", bordercolor="#0f172a")

    app = KoorInstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
