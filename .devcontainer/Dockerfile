# Python公式イメージ（軽量）
FROM python:3.12-slim

# タイムゾーンの設定
ENV TZ=Asia/Tokyo
RUN apt-get update && apt-get install -y tzdata

# 作業ディレクトリ
WORKDIR /app

# 追加
RUN apt-get update && apt-get install -y git && apt-get clean
RUN apt-get update && apt-get install -y procps && apt-get clean

# パッケージインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
# 開発段階ではボリュームのリアルタイム同期あるためいらない
# COPY ./app /app

# 実行ファイル指定
CMD [ "python", "main.py" ]