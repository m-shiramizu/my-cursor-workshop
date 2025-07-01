# 商品管理UI

Streamlitベースの商品管理Web UI

## 機能

- 商品登録フォーム
- 商品検索機能
- API接続状況確認

## 起動方法

```bash
streamlit run main.py --server.port 8501
```

## 環境変数

- `API_URL`: 商品管理APIのURL (デフォルト: http://localhost:8080)

## Cloud Run デプロイ

このディレクトリ全体をCloud Runにデプロイ可能です。
API URLは環境変数で設定してください。