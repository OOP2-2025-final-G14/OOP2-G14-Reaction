import sys
import os
from PySide6.QtWidgets import QApplication
from src.gui.window import MainWindow

# srcディレクトリをパスに通す（モジュールimportのため）
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())