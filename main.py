from ui.main_window import MainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox
import traceback
import sys
import os
os.environ["QT_MEDIA_BACKEND"] = "ffmpeg"


def exception_hook(exc_type, exc_value, exc_tb):
    error_msg = ''.join(traceback.format_exception(
        exc_type, exc_value, exc_tb))
    print(error_msg)
    QMessageBox.critical(None, "Критическая ошибка",
                         f"Программа упала:\n{error_msg}")


def main():
    sys.excepthook = exception_hook

    app = QApplication(sys.argv)

    # Проверяем существует ли атрибут перед использованием
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
