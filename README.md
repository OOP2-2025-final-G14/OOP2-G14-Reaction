# OOP2-G14-Reaction
アプリ名: MojiPop

概要:
--
本アプリは、リアルタイムでリアクションを受け取ることができるデスクトップアプリケーションです。  
GUI で操作でき、QRコードを使ってスマホや別端末からリアクションを送ることができます。  
学内プロジェクトや小規模イベントでの利用を想定しています。
具体的な運用方法としては、講義中またはスピーチ中における傍聴者の反応確認、リアクション送信機能を利用したアンケートの実施

アピールポイント:
--
- 構造がシンプルなので立ち上げに時間がかからない
- とにかくシンプルで直感的な　GUI
- Flask を使ったリアルタイム Web サーバー連携
- URLだけでなく、QRコードで簡単に接続可能
- サーバー停止・起動機能でリアクションの制御も可能

機能説明:
--
サーバー起動機能
-アプリを起動し、タイトルを決めて、サーバー起動することができる

QRコード表示機能
-ホストがQRコードを表示して、ユーザーにリアクション送信画面にアクセスさせることができる

リアクション送信機能
- ユーザーがホストにリアクションを送信できる

リアクション受信機能
- ホストはユーザーから送られてきたリアクションを集計して、円グラフ、ランキングとして確認できる

動作条件: require
--
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
--
1.	プロジェクトのルートに移動（main.py があるフォルダ）。
2.	必要ライブラリをインストール（上記参照）。
3.	ターミナルで以下を実行：python main.py



アプリ画像:
--
サーバー立ち上げ画面
<img width="1470" height="919" alt="スクリーンショット 2026-01-20 16 25 31" src="https://github.com/user-attachments/assets/e162b3d0-fdef-4b4b-86be-871d7196ecdd" />

QRコード表示画面
<img width="1470" height="919" alt="スクリーンショット 2026-01-20 16 25 45" src="https://github.com/user-attachments/assets/dd035234-c8b6-4cf0-bb22-abb253fc408f" />

リアクション送信画面
<img width="1470" height="808" alt="スクリーンショット 2026-01-20 16 21 35" src="https://github.com/user-attachments/assets/f0b2b1ad-fcdd-4538-824c-f3152a8aa897" />

集計円グラフ画面
<img width="1470" height="820" alt="スクリーンショット 2026-01-20 16 22 54" src="https://github.com/user-attachments/assets/8c83fd38-4457-4c03-969c-a40d89449a64" />

集計ランキング画面
<img width="1470" height="828" alt="スクリーンショット 2026-01-20 16 23 13" src="https://github.com/user-attachments/assets/b9543184-0d1a-4721-b312-44da4b05eab3" />
