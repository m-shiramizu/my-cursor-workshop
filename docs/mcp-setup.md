# MCP (Model Context Protocol) 設定ガイド

## 概要

このプロジェクトでは以下のMCPサーバーが設定されています：

- **Cloud Run MCP**: Google Cloud Runへのデプロイ自動化
- **Context7 MCP**: 最新ライブラリドキュメントの取得
- **Playwright MCP**: ブラウザ自動化とWebテスト（新規追加）

## Playwright MCP について

### 特徴

- **高速軽量**: スクリーンショットではなくアクセシビリティツリーを使用
- **LLM対応**: 構造化データで動作（ビジョンモデル不要）
- **決定論的**: 曖昧さのない正確な操作
- **多ブラウザ対応**: Chromium、Firefox、WebKit

### 利用可能な機能

1. **ブラウザ操作**
   - ページナビゲーション
   - クリック、入力、選択操作
   - スクリーンショット撮影

2. **テスト支援**
   - アクセシビリティスナップショット
   - ネットワークリクエスト監視
   - PDF保存

3. **タブ管理**
   - 複数タブの操作
   - タブ間の切り替え

## 設定ファイル

### 基本設定（.mcp.json）

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

### 高度な設定（.mcp-playwright-config.json）

プロジェクトルートに配置された設定ファイルでは以下をカスタマイズ可能：

- **ブラウザ設定**: Chromium、Firefox、WebKitから選択
- **実行モード**: ヘッドレス/ヘッド付き
- **ビューポート**: 画面サイズの指定
- **プロファイル**: 永続化または分離モード

## 使用例

AIとの対話で以下のようにPlaywright機能を活用できます：

### 基本的な操作例

```text
ブラウザでGoogleを開いて、「Cursor AI」を検索してください
```

```text
現在のページのスクリーンショットを撮影してください
```

```text
フォームに商品名「テストアイテム」と価格「100」を入力して送信してください
```

### UI TDD統合での活用例

このワークショップでは、Streamlit UIのTDD開発でPlaywright MCPを活用します：

```text
Playwright MCPを使って、商品管理UIのE2Eテストシナリオを作成してください。

以下のユーザージャーニーをテストしたいです：
1. ブラウザでStreamlitアプリを開く
2. 商品名「テスト商品」、価格「999」を入力  
3. 「商品を登録」ボタンをクリック
4. 登録成功メッセージの確認
5. 商品一覧に新しい商品が表示されることを確認

API: http://localhost:8080（事前起動）
UI: http://localhost:8501（事前起動）
```

#### E2Eテストの特徴

- **統合テスト**: API + UI + ブラウザの連携を包括的にテスト
- **回帰テスト**: UI変更による予期しない副作用の検出
- **ユーザー体験テスト**: 実際のユーザーフローの動作確認
- **自動化**: 手動テストでは困難な複雑シナリオの実行

## セキュリティ注意事項

- **プロファイル保存**: デフォルトでブラウザプロファイルが保存されます
- **ネットワーク制限**: 必要に応じて allowed-origins/blocked-origins を設定
- **分離モード**: テスト時は isolated: true を推奨

## トラブルシューティング

### Node.js要件
- Node.js 18以上が必要
- `node --version` で確認

### 権限エラー
- macOS: セキュリティ設定でブラウザ起動を許可
- Windows: ウイルス対策ソフトの除外設定

### ブラウザインストール
```bash
npx playwright install chromium
```

## 参考リンク

- [Microsoft Playwright MCP 公式](https://github.com/microsoft/playwright-mcp)
- [Playwright ドキュメント](https://playwright.dev/)
- [MCP 仕様](https://modelcontextprotocol.io/)