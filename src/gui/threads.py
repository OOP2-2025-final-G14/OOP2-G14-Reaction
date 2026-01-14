from PySide6.QtCore import QThread, Signal
from src.web.app import create_app
from werkzeug.serving import make_server
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
        self.srv = None

    def update_settings(self, title):
        """設定を更新してFlaskアプリを作成"""
        self.app = create_app(reaction_callback=self.emit_reaction, title=title)

    def emit_reaction(self, emoji):
        """Flaskの中から呼ばれるコールバック"""
        self.reaction_received.emit(emoji)

    def stop(self):
        """サーバーを安全に停止させ、リソースを解放する"""
        if self.srv:
            self.srv.shutdown()
        self.wait()
        print("リアクションサーバーを停止しました。")

    def run(self):
        if self.app:
            try:
                self.srv = make_server(self.host, self.port, self.app)
                self.srv.serve_forever()
            except Exception as e:
                print(f"Flask execution error: {e}")