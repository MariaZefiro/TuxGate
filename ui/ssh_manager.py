import os
import json
from PyQt6.QtCore import QTimer, Qt, QProcess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QScrollArea, QGridLayout, QLabel, QFrame, QMessageBox, QHBoxLayout, QDialog, QFormLayout, QPlainTextEdit, QApplication, QSplitter
)
from PyQt6.QtGui import QMouseEvent, QIcon, QPixmap, QPainter, QPen
from core.theme_manager import ThemeManager

class SSHManager(QWidget):
    def __init__(self):
        super().__init__()
        # Carrega a lista de servidores e inicializa variáveis
        self.servers = self.load_servers()
        self.filtered_servers = self.servers.copy()
        self.ssh_session = None  # Gerenciar a sessão SSH
        self.current_server = None  # Armazena o servidor atualmente conectado
        self.ssh_timer = QTimer(self)  # Timer para processar a saída do pexpect
        self.initUI()

    def load_servers(self):
        # Carrega a lista de servidores a partir de um arquivo JSON
        try:
            with open(os.path.join(os.path.dirname(__file__), "../resources/servers.json"), "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar servidores: {e}")
            return []

    def save_servers(self):
        # Salva a lista de servidores no arquivo JSON
        try:
            with open(os.path.join(os.path.dirname(__file__), "../resources/servers.json"), "w") as file:
                json.dump(self.servers, file, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar servidores: {e}")

    def initUI(self):
        # Configura a interface gráfica principal
        self.setWindowTitle("Gerenciador de Acesso SSH")
        self.setGeometry(100, 100, 1420, 1100)

        main_layout = QVBoxLayout()

        # Criar o splitter para dividir a interface
        self.splitter = QSplitter(Qt.Orientation.Vertical)

        # Parte superior: lista de servidores
        server_layout = QVBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar servidor...")  # Caixa de busca para filtrar servidores
        self.search_box.textChanged.connect(self.filter_servers)
        server_layout.addWidget(self.search_box)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.server_widget = QWidget()
        self.server_layout = QGridLayout()
        self.server_widget.setLayout(self.server_layout)
        self.scroll_area.setWidget(self.server_widget)
        server_layout.addWidget(self.scroll_area)

        button_layout = QHBoxLayout()
        self.add_server_button = QPushButton("Adicionar Servidor")
        self.add_server_button.clicked.connect(self.add_server)
        button_layout.addWidget(self.add_server_button)

        self.theme_button = QPushButton("Alternar Tema")
        self.theme_button.clicked.connect(self.toggle_theme)
        button_layout.addWidget(self.theme_button)

        server_layout.addLayout(button_layout)

        server_widget_container = QWidget()
        server_widget_container.setLayout(server_layout)
        self.splitter.addWidget(server_widget_container)

        # Parte inferior: terminal com altura ajustável
        terminal_layout = QVBoxLayout()
        self.terminal_widget = QFrame(self)
        self.terminal_widget.setStyleSheet("background-color: black; font-family: Arial; color: white;")
        terminal_layout.addWidget(self.terminal_widget)

        terminal_button_layout = QHBoxLayout()
        self.close_connection_button = QPushButton("Fechar Conexão")
        self.close_connection_button.clicked.connect(self.terminate_ssh_session)
        terminal_button_layout.addWidget(self.close_connection_button)

        terminal_layout.addLayout(terminal_button_layout)

        terminal_widget_container = QWidget()
        terminal_widget_container.setLayout(terminal_layout)
        self.splitter.addWidget(terminal_widget_container)

        # Ajustar o comportamento do splitter
        self.splitter.setStretchFactor(0, 1)  # Parte superior (servidores) deve expandir
        self.splitter.setStretchFactor(1, 2)  # Parte inferior (terminal) deve ser ajustável

        # Adicionar o splitter ao layout principal
        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)

        self.dark_mode = False
        self.populate_servers()

    def handle_terminal_input(self, event):
        """Permite digitação no terminal e envia comandos ao pressionar Enter."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.terminal_output.textCursor()
            cursor.movePosition(cursor.MoveOperation.StartOfBlock, cursor.MoveMode.KeepAnchor)
            input_text = cursor.selectedText().strip()
            if input_text:  # Envia apenas se houver texto
                self.send_input_to_terminal(input_text)
            self.terminal_output.appendPlainText("")  # Adiciona nova linha após o envio
        else:
            # Permitir que o QPlainTextEdit lide com outros eventos de teclado, como backspace
            super(QPlainTextEdit, self.terminal_output).keyPressEvent(event)

    def append_to_terminal(self, text):
        """Adiciona texto ao terminal integrado."""
        self.terminal_output.moveCursor(self.terminal_output.textCursor().MoveOperation.End)
        self.terminal_output.insertPlainText(text)
        self.terminal_output.ensureCursorVisible()

    def send_input_to_terminal(self, input_text):
        """Envia entrada do usuário para o terminal SSH."""
        if self.ssh_session:
            self.append_to_terminal(f"{input_text}\n")  # Exibe o texto digitado no terminal

    def populate_servers(self):
        # Atualiza a lista de servidores exibida na interface
        for i in reversed(range(self.server_layout.count())):
            widget = self.server_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for index, server in enumerate(self.filtered_servers):  
            # Cria um "cartão" para cada servidor
            card = QFrame()
            card.setFrameShape(QFrame.Shape.Box)
            card.setLineWidth(1)
            card.setStyleSheet(ThemeManager.get_card_style(self.dark_mode)) 
            card.style().polish(card) 
            card_layout = QVBoxLayout()

            # Adiciona informações do servidor ao cartão
            name_label = QLabel(f"Nome: {server['name']}")
            name_label.setProperty("role", "title")
            ip_label = QLabel(f"IP: {server['ip']}")
            ip_label.setProperty("role", "ip")
            user_label = QLabel(f"Usuário: {server['user']}")

            # Botões de editar e excluir
            edit_button = QPushButton()
            edit_icon_path = os.path.join(os.path.dirname(__file__), "../resources/edit.svg")
            if self.dark_mode:
                edit_icon_path = os.path.join(os.path.dirname(__file__), "../resources/edit_white.svg")  
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setToolTip("Editar servidor")
            edit_button.clicked.connect(lambda _, idx=index: self.edit_server(idx))

            delete_button = QPushButton()  
            delete_icon = QPixmap(16, 16) 
            delete_icon.fill(Qt.GlobalColor.transparent)
            painter = QPainter(delete_icon)
            pen = QPen(Qt.GlobalColor.red)
            pen.setWidth(2)  
            painter.setPen(pen)
            painter.drawLine(2, 2, 14, 14)
            painter.drawLine(14, 2, 2, 14)
            painter.end()
            delete_button.setIcon(QIcon(delete_icon))
            delete_button.setToolTip("Excluir servidor")
            delete_button.clicked.connect(lambda _, idx=index: self.delete_server(idx))  

            button_layout = QHBoxLayout()
            button_layout.addStretch()  
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)

            card_layout.addWidget(name_label)
            card_layout.addWidget(ip_label)
            card_layout.addWidget(user_label)
            card_layout.addLayout(button_layout)  
            card_layout.addStretch()  

            card.setLayout(card_layout)
            card.setObjectName(str(index)) 
            card.mouseDoubleClickEvent = lambda event, idx=index: self.connect_ssh_by_index(idx)

            self.server_layout.addWidget(card, index // 5, index % 5) 

    def edit_server(self, index):
        # Abre um diálogo para editar as informações de um servidor
        server = self.filtered_servers[index]
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Servidor")
        dialog.setModal(True)
        dialog.resize(500, 150)  

        form_layout = QFormLayout()
        name_input = QLineEdit(server["name"])
        ip_input = QLineEdit(server["ip"])
        user_input = QLineEdit(server["user"])
        password_input = QLineEdit(server.get("password", ""))
        password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Nome:", name_input)
        form_layout.addRow("IP:", ip_input)
        form_layout.addRow("Usuário:", user_input)
        form_layout.addRow("Senha:", password_input)

        dialog_buttons = QHBoxLayout()
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(lambda: self.save_edited_server(dialog, index, name_input, ip_input, user_input, password_input))
        dialog_buttons.addWidget(save_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(dialog.reject)
        dialog_buttons.addWidget(cancel_button)

        form_layout.addRow(dialog_buttons)
        dialog.setLayout(form_layout)
        dialog.exec()

    def save_edited_server(self, dialog, index, name_input, ip_input, user_input, password_input):
        # Salva as alterações feitas em um servidor
        name = name_input.text().strip()
        ip = ip_input.text().strip()
        user = user_input.text().strip()
        password = password_input.text().strip()

        if not name or not ip or not user or not password:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios!")
            return

        self.servers[index] = {"name": name, "ip": ip, "user": user, "password": password}
        self.filtered_servers[index] = {"name": name, "ip": ip, "user": user, "password": password}
        self.save_servers()
        self.populate_servers()
        dialog.accept()

    def delete_server(self, index):
        # Exclui um servidor da lista
        server = self.filtered_servers[index]
        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza de que deseja excluir o servidor '{server['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.servers.remove(server)  
            self.filtered_servers.remove(server)  
            self.save_servers()  
            self.populate_servers() 

    def filter_servers(self):
        # Filtra os servidores com base no texto de busca
        search_text = self.search_box.text().lower()
        if not search_text:  
            self.filtered_servers = self.servers.copy()
        else:
            self.filtered_servers = [
                server for server in self.servers
                if search_text in server["name"].lower() or search_text in server["ip"]
            ]
        self.populate_servers()

    def connect_ssh_by_index(self, index):
        # Conecta ao servidor SSH pelo índice
        server = self.filtered_servers[index]
        self.connect_ssh(server)

    def connect_ssh(self, server=None):
        # Conecta ao servidor SSH selecionado
        if not server:
            QMessageBox.warning(self, "Erro", "Selecione um servidor para conectar!")
            return

        if self.ssh_session:
            QMessageBox.warning(self, "Erro", "Já existe uma conexão SSH em andamento!")
            return

        try:
            ssh_command = f"ssh {server['user']}@{server['ip']}"
            self.terminal_process = QProcess(self)
            self.terminal_process.setProgram("xterm")
            self.terminal_process.setArguments([
                "-into", str(int(self.terminal_widget.winId())),
                "-fa", "Arial", "-fs", "12",  # Aumentar o tamanho da fonte
                "-geometry", "160x30",  # Define largura (120 colunas) e altura (30 linhas)
                "-bg", "black",  # Define o fundo como preto
                "-fg", "white",  # Define a cor do texto como branco
                "-hold", "-e", ssh_command
            ])
            self.terminal_process.start()
            self.ssh_session = True  # Marcar que há uma sessão ativa

            # Mostrar o terminal e os botões de controle
            self.terminal_widget.show()
            self.close_connection_button.show()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir o terminal: {e}")
            self.ssh_session = None

    def terminate_ssh_session(self):
        # Encerra a sessão SSH de forma segura
        if hasattr(self, "terminal_process") and self.terminal_process.state() == QProcess.ProcessState.Running:
            self.terminal_process.terminate()
        self.ssh_session = None
        QMessageBox.information(self, "Conexão Encerrada", "A conexão SSH foi encerrada com sucesso.")

    def add_server(self):
        # Abre um diálogo para adicionar um novo servidor
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Servidor")
        dialog.setModal(True)
        dialog.resize(500, 150)  

        form_layout = QFormLayout()
        name_input = QLineEdit()
        ip_input = QLineEdit()
        user_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Nome:", name_input)
        form_layout.addRow("IP:", ip_input)
        form_layout.addRow("Usuário:", user_input)
        form_layout.addRow("Senha:", password_input)

        dialog_buttons = QHBoxLayout()
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(lambda: self.save_new_server(dialog, name_input, ip_input, user_input, password_input))
        dialog_buttons.addWidget(save_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(dialog.reject)
        dialog_buttons.addWidget(cancel_button)

        form_layout.addRow(dialog_buttons)
        dialog.setLayout(form_layout)
        dialog.exec()

    def save_new_server(self, dialog, name_input, ip_input, user_input, password_input):
        # Salva um novo servidor na lista
        name = name_input.text().strip()
        ip = ip_input.text().strip()
        user = user_input.text().strip()
        password = password_input.text().strip()

        if not name or not ip or not user or not password:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios!")
            return

        new_server = {"name": name, "ip": ip, "user": user, "password": password}
        self.servers.append(new_server) 
        self.filtered_servers.append(new_server)  
        self.save_servers()
        self.populate_servers()
        dialog.accept()

    def toggle_theme(self):
        # Alterna entre os temas claro e escuro
        app = QApplication.instance() 
        if self.dark_mode:
            ThemeManager.apply_light_theme(app)
        else:
            ThemeManager.apply_dark_theme(app)
        self.dark_mode = not self.dark_mode
        
        self.populate_servers()  

    def closeEvent(self, event):
        # Encerra a sessão SSH ao fechar a aplicação
        if self.ssh_session:
            self.terminate_ssh_session()
        self.ssh_timer.stop()
        event.accept()