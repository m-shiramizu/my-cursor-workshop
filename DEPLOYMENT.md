# Cloud Run デプロイガイド

## 構成

このプロジェクトはAPIとUIを分離してCloud Runにデプロイするように設計されています。

### ディレクトリ構造

```
.
├── api/           # FastAPI アプリケーション
│   ├── main.py
│   ├── pyproject.toml
│   └── requirements.txt
├── ui/            # Streamlit アプリケーション  
│   ├── main.py
│   ├── pyproject.toml
│   └── requirements.txt
└── src/           # 開発用（レガシー）
```

## デプロイ方法

### 1. API のデプロイ

```bash
# API用 Cloud Run サービスを作成
mcp__cloud-run__deploy_local_folder を使用
- フォルダパス: /path/to/project/api
- サービス名: product-api
- リージョン: asia-northeast1
- ポート: 8080
```

### 2. UI のデプロイ

```bash
# UI用 Cloud Run サービスを作成
mcp__cloud-run__deploy_local_folder を使用
- フォルダパス: /path/to/project/ui  
- サービス名: product-ui
- リージョン: asia-northeast1
- ポート: 8501
- 環境変数: API_URL=https://product-api-xxxxx.a.run.app
```

## 利点

1. **独立性**: APIとUIが完全に独立してスケール可能
2. **最小依存関係**: 各サービスは必要最小限の依存関係のみ
3. **効率的リソース利用**: 各サービスが最適化されたリソースを使用
4. **独立デプロイ**: APIとUIを個別にデプロイ・更新可能

## 注意事項

- Docker は使用しません（Cloud Run のソースベースデプロイを利用）
- 各ディレクトリは独立したPythonプロジェクトです
- UIからAPIへの接続は環境変数 `API_URL` で設定してください
