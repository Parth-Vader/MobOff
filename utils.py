try:
    from Tkinter import Tk
    import tkFileDialog as filedialog
except ImportError:
    from tkinter import Tk, filedialog


def select_directory():
    root = Tk()
    root.withdraw()
    current_directory = filedialog.askdirectory()
    return current_directory
