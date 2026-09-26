import os
import platform
import getpass
import ctypes
import tkinter as tk
import sys
import argparse


ROOT_UID = 0
DEFAULT_FONT_SIZE = 14
FONT_SCALING_STEP = 2
MIN_FONT_SIZE = 6
MAX_FONT_SIZE = 40
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
CURRENT_DIRECTORY = '~'


def parse_arguments(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-vfs', '--virtual_file_system_path', type=str, default=None)
    parser.add_argument('-s', '--script_path', type=str, default=None)
    return parser.parse_args(args)


def is_root() -> bool:
    """Проверка прав суперпользователя для Linux и Windows"""
    try:
        return os.geteuid() == 0
    except AttributeError:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False


def ls(args: list[str]) -> str:
    """Заглушка команды ls"""
    return f"ls {' '.join(arg for arg in args)}"


def cd(args: list[str]) -> str:
    """Заглушка команды cd"""
    return f"cd {' '.join(arg for arg in args)}"


def cout(text: str) -> None:
    """Вывод текста в эмуляторе терминала"""
    terminal.insert(tk.END, text)
    terminal.see(tk.END)


def process_command(command: str) -> None:
    """Исполнение команды"""
    command = command.split()
    if not command:
        return

    if command[0] == "exit":
        if len(command) != 1:
            cout("Слишком много аргументов\n")
            return
        exit_app()
    if command[0] == "ls":
        cout(ls(command[1:]))
    elif command[0] == "cd":
        cout(cd(command[1:]))
    else:
        cout(f"Неизвестная команда {command[0]}")
    cout("\n")


def process_script(script_path: str) -> None:
    if not os.path.exists(script_path):
        cout(f"Скрипт {script_path} не найден\n")
        return

    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    cout(f"{invite}{line}")
                    process_command(line.strip())
                except Exception as e:
                    cout(e)
    except Exception as e:
        cout(e)


def enter(event: tk.Event):
    """Парсинг команд"""
    cout("\n")
    command = terminal.get("input_start", "end-1c").strip()

    if command:
        process_command(command)

    cout(invite)
    terminal.mark_set("input_start", "insert")
    terminal.mark_gravity("input_start", tk.LEFT)
    terminal.see(tk.END)
    return "break"


def backspace(event: tk.Event) -> str | None:
    """Запрет удаления пользовательского приглашения"""
    if terminal.compare("insert", "<=", "input_start"):
        return "break"
    return None


def zoom_in(event: tk.Event) -> str:
    """Увеличивает размер шрифта"""
    font_name, size = terminal.cget("font").split()
    size = int(size)
    if size < MAX_FONT_SIZE:
        terminal.config(font=(font_name, size + FONT_SCALING_STEP))
    return "break"


def zoom_out(event: tk.Event) -> str:
    """Уменьшает размер шрифта"""
    font_name, size = terminal.cget("font").split()
    size = int(size)
    if size > MIN_FONT_SIZE:
        terminal.config(font=(font_name, size - FONT_SCALING_STEP))
    return "break"


def exit_app() -> None:
    if "window" in globals() and window:
        window.destroy()
    sys.exit(0)

username = getpass.getuser()
hostname = platform.node()
symbol = "#" if is_root() else "$"
invite = f"{username}@{hostname}:{CURRENT_DIRECTORY}{symbol} "


def print_debug_info(vfs: str | None, script: str | None) -> None:
    cout("[*] Запуск эмулятора терминала...\n")
    if vfs:
        cout(f"[+] VFS path   : {vfs}\n")
    if script:
        cout(f"[+] Script path: {script}\n")
    cout("-" * 40 + "\n\n")


def main() -> None:
    """Инициализация программы и отрисовка окна"""
    global window, terminal
    args = parse_arguments(sys.argv[1:])
    window = tk.Tk()
    window.title(f"Эмулятор - [{username}@{hostname}]")
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    window.pack_propagate(False)

    terminal = tk.Text(
        window,
        bg="black",
        fg="#00FF00",
        insertbackground="#00FF00",
        font=("monospace", DEFAULT_FONT_SIZE),
    )
    terminal.pack(fill=tk.BOTH, expand=True)

    terminal.bind("<Return>", enter)
    terminal.bind("<BackSpace>", backspace)
    terminal.bind("<Control-equal>", zoom_in)
    terminal.bind("<Control-minus>", zoom_out)

    print_debug_info(args.virtual_file_system_path, args.script_path)

    if args.script_path:
        process_script(args.script_path)

    cout(invite)
    terminal.mark_set("input_start", "insert")
    terminal.mark_gravity("input_start", tk.LEFT)
    terminal.focus_set()
    window.mainloop()


if __name__ == "__main__":
    main()