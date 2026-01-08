from PySide6.QtCore import QThread, Signal
from src.web.app import create_app
import socket

def get_local_ip():
    """ローカルIPアドレスを取得する"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class FlaskServerThread(QThread):
    # GUIスレッドへ送るシグナル
    reaction_received = Signal(str)

    def __init__(self):
        super().__init__()
        self.host = '0.0.0.0'
        self.port = 8080
        self.local_ip = get_local_ip()
        
        # Flaskアプリの作成 (コールバックとしてシグナル発火メソッドを渡す)
        # Flaskアプリはまだ作成しない (タイトル確定後に作成)
        self.app = None

        #False: 動作中, True: 一時停止中
        self.paused = False

    # 一時停止/再開切り替え
    def toggle_pause(self):
        self.paused = not self.paused
        return self.paused

    # 一時停止状態かどうか
    def is_paused(self):
        return self.paused

    def update_settings(self, title):
        """設定を更新してFlaskアプリを作成"""
        self.app = create_app(
            reaction_callback=self.emit_reaction,
            pause_checker=self.is_paused,
            title=title
        )

    def emit_reaction(self, emoji):
        """Flaskの中から呼ばれるコールバック"""
        self.reaction_received.emit(emoji)

    def run(self):
        # スレッド内でFlask起動
        if self.app:
            self.app.run(host=self.host, port=self.port, use_reloader=False)