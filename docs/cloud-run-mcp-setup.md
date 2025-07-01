# Google Cloud Run デプロイセットアップガイド

このドキュメントでは、Cursor Workshop の商品管理アプリケーション（FastAPI + Web UI）をGoogle Cloud Runにデプロイするための設定方法を説明します。セキュリティ上の理由から、サービスアカウントキーを使用せず、よりセキュアな認証方式を採用しています。

## 前提条件

- Google Cloudアカウント
- Google Cloud プロジェクトのセットアップ
- 適切な権限（Cloud Run Admin、Service Account User等）

## 認証方式

### 推奨方式: サービスアカウントインパーソネーション

専用のサービスアカウントを使用し、サービスアカウントキーを使わずにセキュアに認証する方式です。

```bash
gcloud auth application-default login --impersonate-service-account=my-service-account@my-project-id.iam.gserviceaccount.com
```

この方式の利点：

- **セキュリティ**: サービスアカウントキーファイルを管理する必要がない
- **専用権限**: アプリケーションデプロイ用の専用サービスアカウントを使用
- **短期間有効**: 一時的な認証情報を使用
- **監査可能**: インパーソネーションの使用が監査ログに記録される

### 代替方式: Workload Identity Federation（高度な設定）

より高度なセキュリティが必要な場合、Workload Identity Federationを使用できます。

- 外部ID プロバイダー（GitHub Actions、AWS、Azure等）との連携
- 短時間有効なトークンによる認証
- サービスアカウントキーの完全な排除

## 設定手順

### 1. サービスアカウントの作成

Cursor Workshop アプリケーション用の専用サービスアカウントを作成します。

```bash
# プロジェクトIDを設定
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# サービスアカウントを作成
gcloud iam service-accounts create cursor-workshop-app \
    --display-name="Cursor Workshop Application Service Account"

# 必要な権限を付与
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:cursor-workshop-app@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:cursor-workshop-app@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:cursor-workshop-app@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"
```

### 2. インパーソネーション権限の設定

現在のユーザーにサービスアカウントをインパーソネートする権限を付与：

```bash
# Service Account Token Creator ロールを付与
gcloud iam service-accounts add-iam-policy-binding \
    cursor-workshop-app@$PROJECT_ID.iam.gserviceaccount.com \
    --member="user:$(gcloud config get-value account)" \
    --role="roles/iam.serviceAccountTokenCreator"
```

### 3. ローカル環境での認証設定

ローカルPython環境では、ホストの認証情報を直接使用できます。

- **gcloud**: Google Cloud認証情報
- **gh**: GitHub CLI認証情報

これらはホームディレクトリの`.config`フォルダに保存されています。

### 4. サービスアカウントインパーソネーションの設定

ローカル環境で以下のコマンドを実行：

```bash
# サービスアカウントをインパーソネートしてデフォルト認証情報を設定
gcloud auth application-default login \
  --impersonate-service-account=cursor-workshop-app@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## MCP設定ファイルの説明

### Claude Code用 (.mcp.json)

プロジェクトルートの`.mcp.json`はClaude Codeで使用されます。

```json
{
  "mcpServers": {
    "cloud-run": {
      "command": "npx",
      "args": ["-y", "https://github.com/GoogleCloudPlatform/cloud-run-mcp"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

### Cursor用 (.cursor/mcp.json)

`.cursor/mcp.json`はCursorエディタで使用されます。Cloud RunデプロイとContext7（最新ドキュメント取得）の両方の機能を提供します。

## 使用方法

### 初回セットアップ

ローカル環境でインパーソネーション設定を行います：

```bash
# サービスアカウントをインパーソネートしてデフォルト認証情報を設定
gcloud auth application-default login \
  --impersonate-service-account=cursor-workshop-app@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### Claude Codeでの使用

1. ローカル環境で上記の認証設定を完了
2. Claude Codeを起動
3. MCPツールが自動的に読み込まれます
4. 「Deploy to Cloud Run」などのコマンドでアプリケーションデプロイが可能になります

### Cursorでの使用

1. ローカル環境で上記の認証設定を完了
2. Cursorを再起動
3. Settings → MCPでサーバーの状態を確認
4. AIアシスタントを通じてアプリケーションのCloud Runデプロイを実行

## トラブルシューティング

### 認証エラーが発生する場合

```bash
# デフォルト認証情報の確認
gcloud auth application-default print-access-token

# 現在の認証状態を確認
gcloud auth list

# プロジェクトIDの確認
gcloud config get-value project

# アクティブアカウントの確認
gcloud config get-value account

# インパーソネーション権限の確認
gcloud iam service-accounts get-iam-policy cursor-workshop-app@$PROJECT_ID.iam.gserviceaccount.com
```

認証エラーが解決しない場合は、段階的に再設定：

```bash
# 1. ユーザー認証を再実行
gcloud auth login

# 2. プロジェクト設定を確認
gcloud config set project $PROJECT_ID

# 3. アプリケーションデフォルト認証をリセット
gcloud auth application-default revoke

# 4. サービスアカウントインパーソネーションで再認証
gcloud auth application-default login \
  --impersonate-service-account=cursor-workshop-app@$PROJECT_ID.iam.gserviceaccount.com
```

### MCPサーバーが起動しない場合

1. Node.jsがインストールされているか確認
2. npxコマンドが使用可能か確認
3. ログファイルを確認（Cursor: Help → Toggle Developer Tools）
4. デフォルト認証情報が正しく設定されているか確認：

```bash
# 認証情報の存在確認
ls -la ~/.config/gcloud/application_default_credentials.json

# 認証テスト
gcloud auth application-default print-access-token
```

## セキュリティに関する注意事項

- **サービスアカウントキーを使用しない**: インパーソネーションによりキーファイルが不要
- **専用サービスアカウント**: アプリケーションデプロイ専用の権限を持つサービスアカウントを使用
- **最小権限の原則**: 必要最小限の権限のみを付与
- **インパーソネーション権限管理**: Service Account Token Creator権限を適切に管理
- **監査ログ**: インパーソネーションの使用が自動的に記録される
- **定期的な権限レビュー**: 不要な権限を定期的に削除

## 参考リンク

- [Google Cloud Run MCP](https://github.com/GoogleCloudPlatform/cloud-run-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Google Cloud認証ドキュメント](https://cloud.google.com/docs/authentication)
- [サービスアカウントインパーソネーション](https://cloud.google.com/docs/authentication/use-service-account-impersonation)
- [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
