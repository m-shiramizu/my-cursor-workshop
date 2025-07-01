# 商品管理API

FastAPIベースの商品管理REST API

## 機能

- ヘルスチェック (`GET /health`)
- 商品作成 (`POST /items`)
- 商品取得 (`GET /items/{id}`)

## 起動方法

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## API仕様

Swagger UI: http://localhost:8080/docs

## Cloud Run デプロイ

### 必要なファイル構成

```
api/
├── __init__.py      # 空ファイル（必須）
├── main.py         # FastAPIアプリケーション
├── models.py       # Pydanticモデル
├── storage.py      # インメモリストレージ
├── requirements.txt # 依存関係リスト
└── Procfile        # 起動コマンド定義
```

### デプロイ手順

1. **必要なファイルを作成**

```bash
# 空の__init__.pyを作成
touch api/__init__.py

# requirements.txtを生成（プロジェクトルートで実行）
uv pip compile pyproject.toml --extra api -o api/requirements.txt

# Procfileを作成
echo 'web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker main:app' > api/Procfile
```

2. **インポートパスを修正**

すべての相対インポートを絶対インポートに変更:
- `from .models import ...` → `from models import ...`
- `from .storage import ...` → `from storage import ...`

3. **デプロイ実行**

```bash
# プロジェクトルートから実行
gcloud run deploy product-api \
  --source ./api \
  --region asia-northeast1 \
  --allow-unauthenticated
```

### トラブルシューティング

- **ImportError**: 相対インポートが失敗する場合は、すべて絶対インポートに変更
- **Container failed to start**: Procfileの`$PORT`環境変数を確認
- **gunicorn error**: Procfileの引数順序を確認（オプションはmain:appの前に配置）