from flask import Flask, render_template, request, jsonify
from src.db.database import Reaction, init_db, close_db


def create_app(reaction_callback, title="イベント"):
    app = Flask(__name__)
    app.config['TITLE'] = title

    # DB初期化
    init_db()

    # 画面表示
    @app.route('/')
    def index():
        return render_template('index.html', title=app.config['TITLE'])

    
    # リアクション登録
    @app.route('/api/reaction', methods=['POST'])
    def receive_reaction():
        data = request.get_json()
        emoji = data.get("emoji")

        if not emoji:
            return jsonify({"status": "error", "message": "emoji is required"}), 400

        # DB保存（モデルの責務）
        Reaction.add(emoji)

        # GUI（Tkinter / Swing / etc）へ通知
        if reaction_callback:
            reaction_callback(emoji)

        return jsonify({"status": "ok"})


    # 最新リアクション取得
    @app.route('/api/reaction', methods=['GET'])
    def get_reactions():
        reactions = Reaction.latest(limit=20)

        return jsonify([
            {
                "emoji": r.emoji,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for r in reactions
        ])

    
    # 絵文字ごとの集計（オプション）
    @app.route('/api/reaction/summary', methods=['GET'])
    def reaction_summary():
        summary = Reaction.count_by_emoji()

        return jsonify([
            {
                "emoji": row.emoji,
                "count": row.cnt
            }
            for row in summary
        ])

    
    # アプリ終了時の後処理
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_db()

    @app.route('/result')
    def summary_page():
        return render_template('result.html')

    return app
