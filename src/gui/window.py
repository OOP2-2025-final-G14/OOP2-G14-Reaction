from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                               QPushButton, QLabel, QTextEdit, QLineEdit, QGroupBox, QHBoxLayout)
from PySide6.QtCore import Qt
from src.gui.threads import FlaskServerThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアクションボード")
        self.resize(500, 600)

        self._setup_ui()
        
        self.server_thread = FlaskServerThread()
        self.server_thread.reaction_received.connect(self.update_reaction)
        self.is_running = False

    def _setup_ui(self):
        """UIコンポーネントの配置"""
        main_layout = QVBoxLayout()
        
        title_group = QGroupBox("イベント設定")
        title_layout = QVBoxLayout()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("イベントのタイトルを入力してください")
        self.title_input.setStyleSheet("font-size: 16px; padding: 5px;")
        
        title_layout.addWidget(QLabel("タイトル:"))
        title_layout.addWidget(self.title_input)
        title_group.setLayout(title_layout)
        
        server_group = QGroupBox("接続情報")
        server_layout = QVBoxLayout()
        
        self.toggle_button = QPushButton("サーバー起動")
        self.toggle_button.setFixedHeight(40)
        self.toggle_button.clicked.connect(self.toggle_server)
        
        url_layout = QHBoxLayout()
        url_label = QLabel("参加用URL:")
        self.address_display = QLineEdit()
        self.address_display.setReadOnly(True)
        self.address_display.setPlaceholderText("サーバー停止中")
        self.address_display.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.address_display)
        
        server_layout.addWidget(self.toggle_button)
        server_layout.addLayout(url_layout)
        server_group.setLayout(server_layout)

        reaction_group = QGroupBox("受信したリアクション")
        reaction_layout = QVBoxLayout()
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                font-size: 32px;
                font-weight: bold;
                background-color: #ffffff;
            }
        """)
        
        reaction_layout.addWidget(self.log_area)
        reaction_group.setLayout(reaction_layout)

        main_layout.addWidget(title_group)
        main_layout.addWidget(server_group)
        main_layout.addWidget(reaction_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def toggle_server(self):
        if not self.is_running:
            title = self.title_input.text() or "イベント"
            self.title_input.setReadOnly(True)
            self.server_thread.update_settings(title)
            
            self.server_thread.daemon = True
            self.server_thread.start()
            self.is_running = True
            
            ip = self.server_thread.local_ip
            port = self.server_thread.port
            url = f"http://{ip}:{port}"
            
            self.address_display.setText(url)
            self.toggle_button.setText("サーバー稼働中")
            self.toggle_button.setEnabled(False)
            self.log_area.append(f"<span style='font-size: 14px; color: gray;'>--- サーバーを開始しました ---</span>")
        
    def update_reaction(self, emoji):
        self.log_area.append(f"{emoji}")
        
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )