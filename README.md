# Raspberry PiでWordPressを起動（Docker版）

## はじめに：なんでDockerが便利なの？

手動でWordPressを動かすには…

- Apache（Webサーバ）をインストール
- PHPのバージョン管理・モジュール追加
- MariaDB（データベース）をインストール
- DBユーザーとデータベースを手作業で作成
- WordPressをダウンロード＆展開＆配置
- ファイルの権限を設定
- Apacheを再起動して動作確認

これだけやっても **ミスや依存関係トラブルが発生しやすい**。
あとこんなことやってたら初心者は絶対実験時間内に終わらないっす。

### Dockerを使うと？

- たった1ファイル書くだけ
- コマンド1発でWordPress + MariaDBが自動構築
- 設定・構成が明示的で再利用しやすい
- バージョン管理・アップデートも簡単
- とにかく楽。初心者でも失敗しにくい

## このリポジトリで使っているもの

| 名前       | 説明                      | Dockerイメージ       |
|------------|---------------------------|-----------------------|
| WordPress  | ブログCMS本体（PHP製）   | wordpress:latest      |
| MariaDB    | データベース（MySQL互換）| mariadb:10.11         |

## 手順(コピペでOK)

## 日本語環境構築

### 1. Firefoxのインストールと既定ブラウザの設定
日本語入力ができるブラウザを使いたいため，Firefoxをインストールし，既定のブラウザとして設定する。

```bash
sudo apt update
sudo apt install firefox -y
xdg-settings set default-web-browser firefox.desktop
```

### 2. 日本語入力環境（Fcitx + Mozc）のインストール


```bash
sudo apt update
sudo apt install fcitx-mozc -y
```

### インストール後の設定手順

1. 画面右上のキーボードアイコンをクリック

2. 「設定」を開く

3. 左下の「＋」ボタンを押す

4. 一覧から Mozc を選択して追加

必要に応じてログアウト・再ログイン、または再起動を行うと設定が適用されやすくなります。

---
## webサーバー構築&CMSインストール

## Dockerのインストール方法（Raspberry Pi OS）

まずはDockerとDocker Composeのインストールが必要です。以下の手順をターミナルで実行してください。

### 1. Dockerのインストール

```bash
curl -sSL https://get.docker.com | sh
```

### 2. Dockerの自動起動設定と権限追加

```bash
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

※このあと、再ログインまたは再起動してください。

### 3. Docker Composeのインストール

```bash
sudo apt update
sudo apt install -y docker-compose-plugin
```

---

### 1. ファイル作成

```bash
mkdir wordpress-docker && cd wordpress-docker
nano docker-compose.yml
```

### 2. 以下の内容を貼り付けて保存

```yaml
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
```
コピペしてから ctr+O でそのあと Enter 押して(保存)

### 3. 起動

```bash
docker compose up -d
```

### 4. ブラウザで確認

ラズパイのIPアドレスを調べて、以下にアクセス：

```
http://<ラズパイのIPアドレス>:8080
```

WordPressの初期セットアップ画面が表示されたら成功です。

## ボリュームとは？

- `db_data` → MariaDBのデータ保存用
- `wordpress_data` → WordPressのファイル保存用

コンテナを削除してもこのデータは永続化されます。

## おまけ

check.pyでCPUの状態とか調べられる。



