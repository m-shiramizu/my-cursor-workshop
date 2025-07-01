# Cursor Workshop Template

Cursor×Python×GitHub ハンズオン用のテンプレートリポジトリです。

## 📚 ドキュメント

- 📖 [Cursor Workshop ハンズオン資料](docs/cursor-workshop-handson.md) - ワークショップ参加者向けのステップバイステップガイド
- 📋 [プロジェクト要件定義書](docs/requirements.md) - 開発する商品管理APIの仕様
- ☁️ [Cloud Run デプロイセットアップガイド](docs/cloud-run-mcp-setup.md)

## 💻 必要環境

- Python 3.12以上
- [uv](https://github.com/astral-sh/uv) - 高速なPythonパッケージマネージャー
- macOS/Linux/WSL2

## 💡 クイックスタート

### 1. リポジトリのクローン

```bash
git clone https://github.com/YOUR_USERNAME/my-cursor-workshop.git
cd my-cursor-workshop
```

### 2. Python環境のセットアップ

```bash
# 依存関係のインストール
uv sync

# 仮想環境を有効化
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. コマンドリファレンス

| タスク | コマンド |
|------|------|
| 依存関係インストール | `uv sync` |
| テスト実行 | `uv run --frozen pytest` |
| フォーマット | `uv run --frozen ruff format .` |
| Lint | `uv run --frozen ruff check .` |
| FastAPI起動 | `cd api && uv run uvicorn main:app --reload` |
| Streamlit UI起動 | `cd ui && uv run streamlit run main.py` |

## 🛠️ 主な機能

このテンプレートは以下を提供します：

- 🤖 Cursor AIに最適化された設定
- 🚀 モダンなPython開発環境（uv、Ruff、pytest）
- 📝 TDDベースの開発フロー
- 🌐 FastAPI + StreamlitでのWebアプリ開発
- ☁️ Cloud Runへのデプロイを MCPで自動化

## 📁 プロジェクト構造

```text
.
├── api/                 # FastAPI商品管理API
├── ui/                  # Streamlit Web UI
├── tests/               # テストコード
├── docs/                # ドキュメント
├── .cursor/             # Cursor AI設定
├── pyproject.toml       # プロジェクト設定（開発・テスト用）
└── DEPLOYMENT.md        # Cloud Runデプロイガイド
```

## 🚀 開発の始め方

1. [ハンズオン資料](docs/cursor-workshop-handson.md)を開く
2. ステップバイステップで進める
3. AIペアプログラミングを体験！

## 📝 ライセンス

MIT License
