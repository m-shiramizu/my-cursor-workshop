# CLAUDE.md

このファイルは、このリポジトリのコードを扱う際のClaude Code (claude.ai/code)のためのガイダンスを提供します。

## 言語処理の指示

**注意**: Cursorエディタを使用する場合は、`.cursor/rules/`ディレクトリのルールファイルも参照してください。特に以下が重要です：

- `python-structure.mdc`: モダンなPythonプロジェクト構造（srcレイアウト）
- `code-quality-enforcement.mdc`: コード品質と開発ガイドライン
- `development-workflow.mdc`: 開発フローとGitHub統合
- `pep8-enforcement.mdc`: Pythonコーディング標準

## 参考資料

このプロジェクトは以下のリソースに基づいて構築されています：

- **記事**: [DockerでモダンなPython開発環境を構築する](https://zenn.dev/mjun0812/articles/0ae2325d40ed20)
- **テンプレート**: [mjun0812/python-project-template](
  https://github.com/mjun0812/python-project-template)
  - 特に[CLAUDE.md](
    https://github.com/mjun0812/python-project-template/blob/main/CLAUDE.md)の構造を参考にしています

uvの使用、プロジェクト構造など多くの要素が上記のリソースに基づいています。

## プロジェクト概要

これはPythonとFastAPIを使用して**商品管理API**を構築するための
Cursorワークショップテンプレートです。
インメモリストレージを使用したシンプルなREST APIを実装します。

## 主要な要件

APIは以下を実装する必要があります：

- 商品作成（POST /items）
- 商品取得（GET /items/{id}）
- ヘルスチェック（GET /health）
- pytestを使用したTDDアプローチ
- 自動Swagger UI生成を備えたFastAPIフレームワーク

### 商品データ構造

- id: 整数（自動生成）
- name: 文字列（必須、最低1文字）
- price: 浮動小数点数（必須、0より大きい）
- created_at: 日時（自動設定）

## 開発コマンド

### 初回セットアップ

```bash
# ワークショップ用の完全環境セットアップ（推奨）
uv sync --extra all

# または必要な部分のみセットアップ
uv sync --extra dev          # 開発ツールのみ
uv sync --extra api          # API開発のみ  
uv sync --extra ui           # UI開発のみ

# 仮想環境を有効化
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### パッケージ管理

**重要**: 常にuvを使用し、pipは決して使用しないでください

```bash
# ワークショップ環境の同期（推奨）
uv sync --extra all

# 特定のグループのみ同期
uv sync --extra dev --extra api

# 必要に応じて新しい依存関係を追加する場合のみ
# uv add --optional-group api package_name      # API用
# uv add --optional-group ui package_name       # UI用  
# uv add --optional-group dev package_name      # 開発用
```

### アプリケーションの実行

```bash
# FastAPIサーバーの起動（ルートディレクトリから）
uv run --extra api uvicorn api.main:app --reload

# Streamlit UIの起動
uv run --extra ui streamlit run ui/main.py

# Swagger UIへのアクセス: http://localhost:8000/docs
# Streamlit UIへのアクセス: http://localhost:8501
```

### テスト

```bash
# すべてのテストを実行
uv run --extra dev pytest

# 特定のテストファイルを実行
uv run --extra dev pytest tests/test_filename.py

# 詳細出力でテストを実行
uv run --extra dev pytest -v

# anyioプラグインの問題がある場合
PYTEST_DISABLE_PLUGIN_AUTOLOAD="" uv run --extra dev pytest
```

#### FastAPIテストパターン（重要）

httpx 0.27.0以降では、ASGITransportを使用する必要があります：

```python
import httpx
from httpx import ASGITransport
from main import app

# 正しいパターン
@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    with httpx.Client(transport=transport, base_url="http://test") as client:
        yield client

# テストでの使用
def test_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
```

### コード品質チェック

```bash
# コードフォーマット
uv run --extra dev ruff format .

# Lintチェック
uv run --extra dev ruff check .

# Lint問題の修正
uv run --extra dev ruff check . --fix

# 型チェック
uv run --extra dev pyright

# Markdownファイルのチェック（必須）
markdownlint *.md

# pre-commitフックのインストール（初回のみ）
uv run --extra dev pre-commit install

# pre-commitの手動実行
uv run --extra dev pre-commit run --all-files

# pre-commitの自動更新（定期的に実行推奨）
uv run --extra dev pre-commit autoupdate
```

## アーキテクチャに関する注意

- **インメモリストレージ**: データベースなし - データはアプリケーション実行時のみ保持
- **分離デプロイ構造**: APIは`api/`、UIは`ui/`に独立配置（Cloud Run対応）
- **テストコンテキスト**: 分離構造に対応した`tests/context.py`を使用
- **プロジェクト構造**: APIコードは`api/`、UIコードは`ui/`、テストは`tests/`
- **エラーハンドリング**: 適切なバリデーションとHTTPステータスコードの実装
- **認証なし**: このワークショップの範囲外

## 開発フロー

### Issue駆動開発

このプロジェクトはissue駆動開発を採用しています：

1. **要件確認**: docs/requirements.mdなどで要件を確認
2. **タスク分解**: 15-30分で完了可能なタスクに分解
3. **Issue登録**: GitHub CLIを使用して各タスクをissueとして登録
4. **開発**: 各issueごとにブランチを作成し、TDDアプローチで実装
5. **PR作成**: テストの通過を確認後、PRを作成してレビューを依頼

#### ブランチ命名規則

- `feature/task-{issue-number}-{brief-description}`
- 例: `feature/task-1-basic-directories`, `feature/task-2-health-endpoint`

#### 効果的なタスク分解の原則

**推奨タスクサイズ**: 15-30分で完了可能な単位

**良いタスク分解の例:**

- Task 1A: 基本ディレクトリ構造作成 (api/, ui/, tests/)
- Task 1B: 空ファイル作成 (main.py, models.py等)  
- Task 1C: 開発環境セットアップ確認
- Task 2: ヘルスチェックエンドポイント実装
- Task 3: 商品データモデル定義

**避けるべき大きすぎるタスク:**

- ❌ "プロジェクト基盤の構築" (複数の異なる作業を含む)
- ❌ "API全体の実装" (複数エンドポイントを含む)
- ❌ "テストとデプロイの設定" (異なる関心事を含む)

#### GitHub CLI使用例

```bash
# Issueの作成（改行には$'...'構文を使用）
gh issue create -t "タイトル" -b $'## 概要\n実装の説明\n\n## 実装内容\n- [ ] 項目1\n- [ ] 項目2'

# PRの作成
gh pr create \
  --title "feat: 機能名" \
  --body $'## 概要\n変更内容の説明\n\n## 関連Issue\nFixes #1'
```

## TDD（テスト駆動開発）実践ガイド

### t-wada方式TDDの黄金律

**実装コードを書く前に、必ず失敗するテストを書く。**

この原則は機能実装において絶対に破ってはいけません。

### TDD適用の判断基準

**TDDを厳格に適用するタスク（機能実装）:**

- APIエンドポイントの実装
- ビジネスロジックの実装
- データ処理・変換ロジック
- バリデーション機能

**TDDを緩やかに適用するタスク（インフラ・設定）:**

- プロジェクト初期設定（pyproject.toml等）
- ディレクトリ構造の作成
- 設定ファイルの編集
- 依存関係の管理

**重要:** インフラタスクでもTDD適用が可能な場合は実施し、適用が困難な場合は理由を明確に説明すること。

### TDDサイクル

#### 1. Red（失敗するテストを書く）

- 失敗するテストを**1つだけ**書く
- テストの意図が明確になるよう命名する
- 実行して失敗を確認（エラーメッセージを読む）

#### 2. Green（テストを通す）

- テストを通すための**最小限**のコードを書く
- 実装戦略：
  - **仮実装（Fake It）**: まず固定値を返す
  - **三角測量（Triangulation）**: 複数のテストから一般化
  - **明白な実装（Obvious Implementation）**: 自信がある場合のみ

#### 3. Refactor（リファクタリング）

- すべてのテストが通る状態を保つ（グリーンキープ）
- 重複を除去し、設計を改善
- 小さなステップで進める

### TDD実践の重要原則

1. **TODOリストの活用**
   - 実装すべきテストケースをリストとして管理
   - 1つずつ順番に実装

2. **1テスト1アサーション**
   - アサーションルーレットを避ける
   - 複数の検証が必要なら、テストを分割

3. **段階的な実装**
   - 仮実装 → 三角測量 → 一般化の順で進める

4. **テストピラミッドの実践**
   - **Unit Tests（単体テスト）**: 個別機能の詳細検証
   - **Integration Tests（統合テスト）**: コンポーネント間連携
   - **E2E Tests（エンドツーエンドテスト）**: ユーザージャーニー全体

### 実践例

```python
# ステップ1: Red（失敗するテスト）
import pytest
from httpx import ASGITransport, AsyncClient
from api.main import app

@pytest.mark.anyio
async def test_create_product_returns_201():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as client:
        response = await client.post("/items", json={"name": "商品", "price": 100})
    assert response.status_code == 201  # 失敗

# ステップ2: Green（最小限の実装）
@app.post("/items", status_code=201)
async def create_item():
    return {}  # 仮実装

# ステップ3: 次のテストを追加してリファクタリング
```

### FastAPI + httpx テストパターン（標準）

```python
# tests/api/test_main.py の標準テンプレート
import pytest
from httpx import ASGITransport, AsyncClient
from api.main import app

@pytest.mark.anyio
async def test_endpoint_name():
    """エンドポイントのテスト説明"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # テスト実装
        response = await client.get("/path")
        assert response.status_code == 200
```

### コミット戦略

- Red: `git commit -m "test: add test for ..."`
- Green: `git commit -m "feat: implement minimal ..."`  
- Refactor: `git commit -m "refactor: extract ..."`

### Playwright統合TDDの実践

**UI開発におけるTDD拡張**: ワークショップではStreamlit UIの開発でPlaywright MCPを活用

#### E2Eテストサイクル

1. **Red（失敗するE2Eテスト）**
   - ユーザージャーニーシナリオの定義
   - ブラウザ自動化での操作フロー記述
   - 期待する結果の明文化

2. **Green（E2Eテストを通す）**
   - StreamlitアプリとAPIの実装
   - フォーム、表示機能の最小実装
   - ブラウザテストの成功確認

3. **Refactor（UI/UX改善）**
   - デザインの洗練
   - ユーザビリティの向上
   - パフォーマンス最適化

#### 統合テスト戦略

- **API Layer**: FastAPIの単体・統合テスト
- **UI Layer**: Streamlitコンポーネントテスト
- **E2E Layer**: Playwright MCPによるブラウザ自動化

### 重要原則：手動テスト実行によるTDD品質保証

**TDD品質保証ルール**: 以下の場合は必ず手動でテストを実行してグリーンを確認する

1. 機能実装コードを変更した場合
2. pre-commitフックが自動修正を行った場合  
3. pre-commitでエラーが発生して手動修正した場合

```bash
# 機能実装後やpre-commit修正後の確認手順
uv run --extra dev pytest  # 手動でテスト実行
# → 全テストがグリーンであることを確認してからコミット

git add .
git commit -m "..."  # テスト通過を確認してからコミット
```

**重要な変更**: pre-commitは自動的にテストを実行しなくなりました。これにより：

- ワークショップ中の予期しない中断を防止
- 開発者が意図したタイミングでのテスト実行
- TDD学習により集中できる環境

**AIは必ず**機能実装やコード修正後に手動でpytestを実行し、グリーン状態を確認してからコミットすること。

## 開発ガイドライン

### コード品質要件

- **型ヒント**: すべてのコードで必須
- **ドキュメント**: パブリックAPIで必須
- **関数設計**: 小さく、焦点を絞った関数
- **行長制限**: 最大100文字
- **テスト**: 新機能とバグ修正で必須
- **Markdown**: ファイル編集後は常にmarkdownlintでチェックし、エラーがゼロであることを確認

### パッケージ管理ルール

- **必須**: uvのみを使用、pipは禁止
- **基本操作**: まず`uv sync`でプロジェクトを同期（pyproject.tomlから自動認識）
- **新規追加**: 必要な場合のみ`uv add package` / `uv add --dev package`
- **ツール実行**: `uv run tool`
- **禁止**: `uv pip install`、既存の依存関係の重複追加、`@latest`構文

**重要**: pyproject.tomlで依存関係がすでに定義されている場合は、
`uv add`で重複追加せず、`uv sync`のみを使用してください

#### パッケージ管理緊急対応プロトコル（必須遵守）

**テストライブラリ不足エラーの場合：**

##### 手順1: 環境確認（必須）

```bash
pwd  # プロジェクトルートにいることを確認
cat pyproject.toml | grep -A 10 "dev"  # 既存依存関係を確認
```

##### 手順2: ルート環境への統一追加

```bash
# 絶対にapi/やui/ではなく、プロジェクトルートで実行
uv add --dev pytest httpx asgi-lifespan trio fastapi
uv sync
```

##### 手順3: 検証（必須）

```bash
uv run --frozen pytest tests/ --collect-only  # テスト収集確認
uv run --frozen pytest tests/api/ -v  # 実際のテスト実行
```

**絶対禁止事項:**

- ❌ 異なるディレクトリでの`uv add`後、別ディレクトリでのテスト実行
- ❌ `cd api && uv add` → `cd .. && pytest`のような環境混在
- ❌ エラー時の応急処置的なパッケージ追加

**AI開発者への強制指示:**

1. パッケージ追加前に必ず`pwd && ls pyproject.toml`で位置確認
2. 「なぜこのパッケージが必要か」を明確に説明
3. 「どこに追加すべきか」の判断根拠を提示
4. 環境不整合時は`uv sync`による再構築を最優先

#### 依存関係配置の明確なルール

```text
pyproject.toml (ルート) - テスト実行環境
├── dependencies: 共通ライブラリ
├── dev-dependencies: テスト・開発ツール全般
│   ├── pytest, httpx, asgi-lifespan, trio
│   ├── ruff, pyright, pre-commit
│   └── markdownlint-cli
│
api/pyproject.toml - 本番デプロイ用
├── dependencies: FastAPI実行に必要な最小限のみ
│   ├── fastapi>=0.100.0
│   ├── uvicorn[standard]>=0.23.0
│   └── pydantic>=2.0.0
│
ui/pyproject.toml - 本番デプロイ用
├── dependencies: Streamlit実行に必要な最小限のみ
│   ├── streamlit>=1.28.0
│   └── pydantic>=2.0.0
```

**実行コマンド統一（厳格に遵守）:**

- テスト: `uv run --frozen pytest` （常にプロジェクトルートから）
- API開発: `cd api && uv run uvicorn main:app --reload`
- UI開発: `cd ui && uv run streamlit run main.py`

### テスト要件

- **フレームワーク**: `uv run --frozen pytest`
- **非同期テスト**: anyioを使用、asyncioは禁止
- **カバレッジ**: エッジケースとエラーケース
- **TDD実践**: t-wada氏推奨の方式を厳格に適用（詳細は下記TDDセクション参照）

## 技術的制約

- Python 3.12以上が必要
- ローカルPython環境での開発（Docker不要）
- 外部データベースなし
- 認証/認可なし
- 更新/削除操作なし（作成と読み取りのみ）
- 自動生成ドキュメントを備えたREST API用のFastAPI
- Cloud RunへのデプロイはMCP経由で自動化

## Cloud Run デプロイ

### 手動デプロイ方法（gcloudコマンド）

Cloud Runへのデプロイは、MCPを使用せずに直接gcloudコマンドで行うことも可能です。

#### 必須の事前準備

1. **api/__init__.py を作成**
   ```bash
   # 空のファイルを作成（Pythonパッケージとして認識させるため）
   touch api/__init__.py
   ```

2. **api/requirements.txt を作成**
   ```bash
   # プロジェクトルートで実行
   uv pip compile pyproject.toml --extra api -o api/requirements.txt
   ```

3. **api/Procfile を作成**
   ```bash
   # api/Procfile の内容:
   echo 'web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker main:app' > api/Procfile
   ```

4. **インポートパスを絶対インポートに変更（重要）**
   - ❌ `from .models import ProductModel`（相対インポート）
   - ✅ `from models import ProductModel`（絶対インポート）
   
   **理由**: Cloud Run環境では相対インポートが失敗するため

#### gcloudコマンドでのデプロイ

```bash
# プロジェクトルートから実行
gcloud run deploy product-api \
  --source ./api \
  --region asia-northeast1 \
  --allow-unauthenticated
```

### MCPでのデプロイ（代替方法）

MCPを使用する場合も、上記の事前準備を完了してから実行してください。

```
mcp__cloud-run__deploy_local_folder
- folderPath: ./api
- project: YOUR_PROJECT_ID
- region: asia-northeast1
```

### トラブルシューティング

#### ImportError: attempted relative import
- **原因**: Cloud Run環境で相対インポートが失敗
- **解決**: すべてのインポートを絶対インポートに変更

#### gunicorn: error: unrecognized arguments
- **原因**: Procfileの引数順序が不適切
- **解決**: 上記のProcfile例を正確にコピー

#### Container failed to start
- **原因**: ポート設定の問題
- **解決**: Procfileで必ず`$PORT`環境変数を使用

### Cloud Run 分離デプロイ要件

**重要**: Cloud Run デプロイ時は、APIとUIを分離した独立構造で実装してください：

#### ワークショップ用のシンプル構造

```text
project/
├── pyproject.toml      # 統合された依存関係管理
├── api/
│   ├── main.py         # FastAPIアプリケーション
│   └── README.md
├── ui/
│   ├── main.py         # Streamlitアプリケーション
│   └── README.md
└── tests/              # テストファイル
```

#### 依存関係管理

**統合pyproject.toml**: オプショナルグループで管理

- `[project.optional-dependencies.api]`: FastAPI用
- `[project.optional-dependencies.ui]`: Streamlit用  
- `[project.optional-dependencies.dev]`: 開発・テスト用
- `[project.optional-dependencies.all]`: 全て含む（ワークショップ推奨）

#### デプロイ方法

個別デプロイ時は各ディレクトリを `mcp__cloud-run__deploy_local_folder` で実行

## Gitコミットガイドライン

- ユーザーレポートに基づくバグ修正や機能の場合：

  ```bash
  git commit --trailer "Reported-by:<name>"
  ```

- GitHub Issueに関連する場合：

  ```bash
  git commit --trailer "Github-Issue:#<number>"
  ```

- **禁止**: `co-authored-by`やツール使用への言及は絶対に避ける

## プルリクエスト

- 変更の詳細な説明を含める
- 解決される問題とその解決方法に焦点を当てる
- **禁止**: `co-authored-by`やツール使用への言及は絶対に避ける

## エラー解決

### CI失敗の解決順序

1. フォーマットの修正
2. 型エラーの修正
3. Lintエラーの修正

### 一般的な問題

- **行長制限**: 括弧で文字列を分割、複数行の関数呼び出し、インポートの分割
- **型エラー**: Optional、型の絞り込み、関数シグネチャの確認をチェック
- **pytest実行失敗**: まず`uv sync`を実行、既存の依存関係を重複させない
- **カバレッジ測定失敗**: pyproject.tomlですでに設定済み、追加の設定ファイルは不要
- **Pytest**: anyio pytestマークが見つからない場合は、`PYTEST_DISABLE_PLUGIN_AUTOLOAD=""`を追加

### ベストプラクティス

- コミット前にgit statusをチェック
- 型チェック前にフォーマッタを実行
- Markdownファイル編集後は常にmarkdownlintを実行
- 変更を最小限に保つ
- 既存のパターンに従う
- パブリックAPIは常にドキュメント化

## AI開発時のコミュニケーションガイドライン

### CLI環境での応答スタイル

**基本原則**: Claude Codeは**コマンドライン環境**で使用されるため、応答は簡潔かつ要点を絞ること

**適切な応答例:**

```
✅ "pyproject.toml統合完了。pre-commit最適化に進みます。"
✅ "ファイル編集完了。テスト実行中..."
✅ "エラー修正。再度コミットします。"
```

**避けるべき冗長な応答例:**

```
❌ "はい、承知いたしました。それでは...という手順で進めてまいります。
   まず最初に...について詳しく説明いたします。普段私たちが..."
❌ "詳細な手順をご説明します。ステップ1として...ステップ2として..."
```

### レスポンス長の目安

- **通常応答**: 1-3行以内
- **エラー説明**: 最大5行以内  
- **計画説明**: 箇条書きで最大10行以内
- **技術解説**: 初心者向けでも最大15行以内

### ワークショップ進行での配慮

- **進捗報告**: 現在のタスクと次のステップを明示
- **エラー対応**: 原因と解決策を簡潔に説明
- **学習サポート**: 必要最小限の技術解説のみ

## 重要な指示のリマインダー

求められたことだけを行い、それ以上でも以下でもありません。

目標を達成するために絶対に必要でない限り、決してファイルを作成しないでください。

常に新しいファイルを作成するよりも既存のファイルを編集することを優先してください。

決して積極的にドキュメントファイル（*.md）やREADMEファイルを作成しないでください。
ユーザーから明示的に要求された場合にのみドキュメントファイルを作成してください。

## important-instruction-reminders

求められたことだけを行い、それ以上でも以下でもありません。
目標を達成するために絶対に必要でない限り、決してファイルを作成しないでください。
常に新しいファイルを作成するよりも既存のファイルを編集することを優先してください。
決して積極的にドキュメントファイル（*.md）やREADMEファイルを作成しないでください。
ユーザーから明示的に要求された場合にのみドキュメントファイルを作成してください。
