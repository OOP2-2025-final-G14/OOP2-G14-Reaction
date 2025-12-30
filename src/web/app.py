from flask import Flask, render_template, request, jsonify
from src.db.database import Reaction, init_db

def create_app(reaction_callback):
    app = Flask(__name__)

    # DB初期化
    init_db()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/reaction', methods=['POST'])
    def receive_reaction():
        data = request.get_json()
        emoji = data.get("emoji")

        if not emoji:
            return jsonify({"status": "error"}), 400

        # 保存
        Reaction.create(emoji=emoji)

        # GUIへ通知
        reaction_callback(emoji)

        return jsonify({"status": "ok"})

    @app.route('/api/reaction', methods=['GET'])
    def get_reactions():
        reactions = (
            Reaction
            .select()
            .order_by(Reaction.created_at.desc())
        )

        return jsonify([
            {
                "emoji": r.emoji,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for r in reactions
        ])

    return app
