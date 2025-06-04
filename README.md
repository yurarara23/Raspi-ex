Raspberry PiでWordPressを爆速起動する方法（Docker版）

はじめに：なんでDockerが便利なの？
手動でWordPressを動かすには…
Apache（Webサーバ）をインストール

PHPのバージョン管理・モジュール追加

MariaDB（データベース）をインストール

DBユーザーとデータベースを手作業で作成

WordPressをダウンロード＆展開＆配置

ファイルの権限を設定

Apacheを再起動して動作確認
これだけやっても **ミスや依存関係トラブルが発生しやすい**

Dockerを使うと？
たった1ファイル書くだけ
コマンド1発でWordPress + MariaDBが自動構築
設定・構成が明示的で再利用しやすい
バージョン管理・アップデートも簡単
とにかく楽。初心者でも失敗しにくい！

📦 このリポジトリで使っているもの
名前	説明	Dockerイメージ
WordPress	ブログCMS本体（PHP製）	wordpress:latest
MariaDB	データベース（MySQL互換）	mariadb:10.11

🛠️ インストール手順（超カンタン）
1. ファイル作成
bash
コピーする
編集する
mkdir wordpress-docker && cd wordpress-docker
nano docker-compose.yml
2. 以下の内容を貼り付けて保存（Ctrl+O → Enter → Ctrl+X）
yaml
コピーする
編集する
version: '3.8'

services:
  db:
    image: mariadb:10.11
    restart: always
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wpuser
      MYSQL_PASSWORD: wppassword
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - db_data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    restart: always
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppassword
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress_data:/var/www/html

volumes:
  db_data:
  wordpress_data:
3. 起動（たった1行！）
bash
コピーする
編集する
docker compose up -d
4. ブラウザで確認！
ラズパイのIPアドレスを調べて、以下にアクセス：

cpp
コピーする
編集する
http://<ラズパイのIPアドレス>:8080
WordPressの初期セットアップ画面が表示されたら成功です🎉

📁 ボリュームとは？
db_data → MariaDBのデータ保存用

wordpress_data → WordPressのファイル保存用

コンテナを削除してもこのデータは永続化されます。

🛡️ 補足：公開時の注意点
公開用に使うなら ルーターでポート8080 → 80に変更 するのがオススメ

HTTPS を使う場合は Nginx + Let's Encrypt構成も検討

WordPressのセキュリティ強化（ログイン制限・バックアップ）も忘れずに！

📚 参考
WordPress Docker公式

MariaDB Docker公式

✨ ラズパイ初心者でも大丈夫！
Dockerを使えば、環境構築のミスを恐れる必要なし。トラブルも起きにくく、やり直しも簡単。
あなたのラズパイが、すぐにパーソナルなブログサーバになります😊