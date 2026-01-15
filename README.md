# OOP2-G14-Reaction
アプリ名: Recaction

概要:
リアルタイムでリアクションを受け取ることができるデスクトップアプリケーションです。  
GUI で操作でき、QRコードを使ってスマホや別端末からリアクションを送ることができます。  
学内プロジェクトや小規模イベントでの利用を想定しています。

アピールポイント
- PySide6 によるシンプルで直感的な GUI
- Flask を使ったリアルタイム Web サーバー連携
- QRコードで簡単に接続可能
- SQLite + Peewee による軽量データベース管理
- 一時停止機能でリアクションの制御も可能

動作条件: require

python 3.17

以下をpip install
- Flask 3.1.2
- peewee 3.18.3
- pyside6 6.10.0
- pyside6_addons 6.10.0
- pyside6_essentials 6.10.0
- qrcode 8.2
- Werkzeug 3.1.5

実行手順
1.	プロジェクトのルートに移動（main.py があるフォルダ）。
2.	必要ライブラリをインストール（上記参照）。
3.	ターミナルで以下を実行：python main.py
