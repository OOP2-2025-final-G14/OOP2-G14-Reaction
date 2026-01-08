import qrcode
from io import BytesIO
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                               QPushButton, QLabel, QTextEdit, QLineEdit, QGroupBox, QHBoxLayout, QMessageBox)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from src.gui.threads import FlaskServerThread
from src.db.database import Reaction

class QRWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QRコード")
        self.resize(300, 300)
        
        layout = QVBoxLayout()
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qr_label)
        self.setLayout(layout)

    def set_qr_code(self, url):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # PIL Image to QPixmap
        im_data = img.convert("RGBA").tobytes("raw", "RGBA")
        qim = QImage(im_data, img.size[0], img.size[1], QImage.Format.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qim)
        
        self.qr_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアクションボード")
        self.resize(500, 600)

        self._setup_ui()
        
        self.server_thread = FlaskServerThread()
        self.server_thread.reaction_received.connect(self.update_reaction)
        self.is_running = False
        self.qr_window = None

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
        
        self.qr_button = QPushButton("QR表示")
        self.qr_button.clicked.connect(self.show_qr_code)
        self.qr_button.setEnabled(False)
        url_layout.addWidget(self.qr_button)
        
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
        
        reset_button = QPushButton("データベースとログをリセット")
        reset_button.clicked.connect(self.reset_db)
        reaction_layout.addWidget(reset_button)
        
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
            self.qr_button.setEnabled(True)
            self.log_area.append(f"<span style='font-size: 14px; color: gray;'>--- サーバーを開始しました ---</span>")

    def show_qr_code(self):
        url = self.address_display.text()
        if url and url != "サーバー停止中":
            if not self.qr_window:
                self.qr_window = QRWindow()
            self.qr_window.set_qr_code(url)
            self.qr_window.show()
        
    def update_reaction(self, emoji):
        self.log_area.append(f"{emoji}")
        
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )
        
    def reset_db(self):
        ret = QMessageBox.question(self, "確認", "データベースとログを完全に削除しますか？",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ret == QMessageBox.Yes:
            Reaction.reset_all()
            self.log_area.clear()
            self.log_area.append(f"<span style='font-size: 14px; color: gray;'>--- データベースをリセットしました ---</span>")