from flask import Flask, render_template, request, jsonify
from src.db.database import Reaction, init_db, close_db


def create_app(reaction_callback, title="イベント"):
    app = Flask(__name__)
    app.config['TITLE'] = title
    #一時停止ボタン
    app.config['PAUSED'] = False

    # DB初期化
    init_db()

    # 画面表示
    @app.route('/')
    def index():
        return render_template('index.html', title=app.config['TITLE'])

    
    # リアクション登録
    @app.route('/api/reaction', methods=['POST'])
    def receive_reaction():
        #　一時停止
        if app.config['PAUSED']:
            return jsonify({"status": "paused",
                            "message": "リアクションは一時停止中です"}), 403 # 禁止されているというステータスコード

        # データ受信
        data = request.get_json()
        topic = data.get("topic", "default")
        emoji = data.get("emoji")

        # 入力チェック
        if not emoji:
            return jsonify({"status": "error",
                            "message": "emoji is required"}), 400
        

        # DB保存（モデルの責務）
        Reaction.add(topic, emoji)

        # GUI（Tkinter / Swing / etc）へ通知
        if reaction_callback:
            reaction_callback(emoji)

        return jsonify({"status": "ok"})

    # 一時停止トグル(ホスト専用API)
    @app.route('/api/pause', methods=['POST'])
    #ON/OFF切り替え
    def toggle_pause():
        #状態の切り替え
        app.config['PAUSED'] = not app.config['PAUSED']
        return jsonify({
            "paused": app.config['PAUSED']
        })



    # 最新リアクション取得
    @app.route('/api/reaction', methods=['GET'])
    def get_reactions():
        topic = request.args.get("topic", "default")
        reactions = Reaction.latest(topic, limit=20)

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
        topic = request.args.get("topic", "default")
        summary = Reaction.count_by_emoji(topic)

        return jsonify([
            {
                "emoji": row.emoji,
                "count": row.cnt
            }
            for row in summary
        ])
    
    @app.route("/api/topic", methods=["POST"])
    def change_topic():
        data = request.get_json()
        new_topic = data.get("topic")

        if not new_topic:
            return jsonify({
                "status": "error",
                "message": "topic is required"
            }), 400

        # ★ お題変更時にそのお題のデータを削除
        Reaction.reset_topic(new_topic)

        return jsonify({
            "status": "ok",
            "topic": new_topic
        })

    
    # アプリ終了時の後処理
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_db()

    @app.route('/result')
    def summary_page():
        return render_template('result.html')

    return app
