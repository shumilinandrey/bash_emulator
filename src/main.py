import os
import tkinter as tk
import sys


ROOT_UID = 0
DEFAULT_FONT_SIZE = 14
FONT_SCALING_STEP = 2
MIN_FONT_SIZE = 6
MAX_FONT_SIZE = 40
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800


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


def enter(event: tk.Event):
    """Парсинг команд"""
    command = terminal.get("input_start", "end-1c").strip()
    if command == "exit":
        exit_app()

    if command:
        command = command.split()
        cout("\n")
        if command[0] == "ls":
            cout(ls(command[1:]))
        elif command[0] == "cd":
            cout(cd(command[1:]))
        else:
            cout(f"Неизвестная команда {command[0]}")
        cout("\n")

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


username = os.getlogin()
hostname = os.uname().nodename
symbol = "#" if os.geteuid() == ROOT_UID else "$"
invite = f"{username}@{hostname}{symbol} "


def main() -> None:
    """Инициализация программы и отрисовка окна"""
    global window, terminal
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
    cout(invite)
    terminal.mark_set("input_start", "insert")
    terminal.mark_gravity("input_start", tk.LEFT)
    terminal.focus_set()
    window.mainloop()


if __name__ == "__main__":
    main()