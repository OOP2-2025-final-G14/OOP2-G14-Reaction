from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                               QPushButton, QLabel, QTextEdit)
from PySide6.QtCore import Qt
from src.gui.threads import FlaskServerThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアクションボード")
        self.resize(400, 500)

        self._setup_ui()
        
        # サーバー用スレッドの準備
        self.server_thread = FlaskServerThread()
        self.server_thread.reaction_received.connect(self.update_reaction)
        self.is_running = False

    def _setup_ui(self):
        """UIコンポーネントの配置"""
        layout = QVBoxLayout()
        
        self.status_label = QLabel("サーバー停止中")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")
        
        self.toggle_button = QPushButton("サーバー起動")
        self.toggle_button.setFixedHeight(50)
        self.toggle_button.clicked.connect(self.toggle_server)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("font-size: 24px;")

        layout.addWidget(self.status_label)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.log_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_server(self):
        if not self.is_running:
            self.server_thread.daemon = True
            self.server_thread.start()
            self.is_running = True
            
            ip = self.server_thread.local_ip
            port = self.server_thread.port
            url = f"http://{ip}:{port}"
            
            self.status_label.setText(f"稼働中: {url}\n(スマホでアクセスしてください)")
            self.toggle_button.setText("サーバー稼働中")
            self.toggle_button.setEnabled(False)
            self.log_area.append(f"--- サーバーを開始しました ---\nURL: {url}")
        
    def update_reaction(self, emoji):
        self.log_area.append(f"受信: {emoji}")
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )