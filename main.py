import sys
from PyQt6.QtWidgets import QApplication
from ui.ssh_manager import SSHManager

if __name__ == "__main__":
    # Cria uma instância do aplicativo Qt
    app = QApplication(sys.argv)

    # Cria a janela principal do aplicativo
    window = SSHManager()
    window.show()
    sys.exit(app.exec())
