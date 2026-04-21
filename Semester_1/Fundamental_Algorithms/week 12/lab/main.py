import unittest
from tkinter import Tk

from ui.gui import PenguinGUI


def run_tests() -> bool:
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_gui():
    root = Tk()
    root.geometry("900x600")
    app = PenguinGUI(master=root)
    app.mainloop()


def main():
    ok = run_tests()
    if ok:
        print("\nRan successfully.\n")
        run_gui()
    else:
        print("\nTests failed.\n")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
