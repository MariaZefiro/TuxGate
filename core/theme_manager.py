from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class ThemeManager:
    @staticmethod
    def apply_light_theme(widget):
        light_theme = """
        QWidget { background-color: #f7f7f7; color: #2c2c2c; font-family: Arial, sans-serif; font-size: 14px; }
        QLineEdit, QTextEdit, QComboBox, QInputDialog, QGroupBox {
            background-color: #f0f0f0; color: #2c2c2c; border: 1px solid #cccccc; border-radius: 5px; padding: 2px;
        }
        QPushButton { background-color: #e4e4e4; color: #2c2c2c; border: 1px solid #bbbbbb; border-radius: 5px; padding: 5px; }
        QPushButton:hover { background-color: #d4d4d4; }
        QLabel { color: #2c2c2c; }
        QMessageBox { background-color: #f7f7f7; color: #2c2c2c; width: 300px; }
        svg { color: blue; }  /* Set SVG color to blue for light theme */
        """
        widget.setStyleSheet(light_theme)

    @staticmethod
    def apply_dark_theme(widget):
        dark_theme = """
        QWidget { background-color: #1e1e2f; color: #dcdcdc; font-family: Arial, sans-serif; font-size: 14px; }
        QLineEdit, QTextEdit, QComboBox, QInputDialog, QGroupBox {
            background-color: #2e2e3f; color: #dcdcdc; border: 1px solid #44475a; border-radius: 5px; padding: 2px;
        }
        QPushButton { background-color: #44475a; color: #ffffff; border: 1px solid #6272a4; border-radius: 5px; padding: 5px; }
        QPushButton:hover { background-color: #6272a4;  width: 300px;  }
        QLabel { color: #ffffff; }
        QMessageBox { background-color: #1e1e2f; color: #dcdcdc; }
        svg { color: white; }  /* Set SVG color to white for dark theme */
        """
        widget.setStyleSheet(dark_theme)

    @staticmethod
    def get_card_style(dark_mode=False):
        if dark_mode:
            return """
            QFrame {
                border: 1px solid #44475a; 
                border-radius: 10px;
                background-color: #2e2e3f !important;
                padding: 15px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5); 
                transition: transform 0.2s, box-shadow 0.2s; 
            }
            QFrame:hover {
                transform: scale(1.02);
                box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.7); 
            }
            QLabel {
                font-size: 14px;
                color: #dcdcdc; 
            }
            QLabel[role='title'] {
                font-weight: bold;
                font-size: 16px;
                color: #ffffff; 
            }
            """
        else:
            return """
            QFrame {
                border: 1px solid #dcdcdc; 
                border-radius: 10px;
                background-color: #ffffff; 
                padding: 15px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                transition: transform 0.2s, box-shadow 0.2s; 
            }
            QFrame:hover {
                transform: scale(1.02);
                box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.2); 
            }
            QLabel {
                font-size: 14px;
                color: #333333; 
            }
            QLabel[role='title'] {
                font-weight: bold;
                font-size: 16px;
                color: #4f4e4e; 
            }
            """
