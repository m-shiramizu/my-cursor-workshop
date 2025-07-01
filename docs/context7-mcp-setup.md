# Context7 MCP セットアップガイド

このドキュメントでは、Context7 MCPをClaude CodeとCursorエディタで使用するための設定方法を説明します。

## Context7 MCPとは

Context7は、バージョン対応のドキュメントを開発ワークフローに直接統合するMCP（Model Context Protocol）サーバーです。

### 主要機能

- **バージョン対応ドキュメント**: 最新の公式ドキュメントを動的に取得
- **リアルタイム更新**: ライブラリの最新バージョンに対応したコード例を提供
- **AI統合**: プロンプトに`use context7`を追加するだけで最新情報を取得
- **幅広い互換性**: Claude Desktop、Cursor、Windsurf等のMCP対応クライアントで利用可能

### 解決する問題

- **古い情報**: 過去のバージョンのAPIや廃止されたメソッドの使用を防止
- **不正確な情報**: 存在しない関数のハルシネーションを防止
- **一般的すぎる情報**: 特定のライブラリバージョンに最適化されたコード例を提供

## 前提条件

- Node.js 18以上
- MCP対応クライアント（Claude Code、Cursor等）

## 設定済み内容

このプロジェクトでは、Context7 MCPが既に設定されています：

### Claude Code用 (.mcp.json)

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

### Cursor用 (.cursor/mcp.json)

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

## 使用方法

### 基本的な使用法

プロンプトに`use context7`を追加するだけで、最新のドキュメントを取得できます：

```text
use context7

FastAPIでAPIエンドポイントを作成する方法を教えてください
```

### 具体的な使用例

#### 1. ライブラリのドキュメント取得

```text
use context7

Pydanticのバリデーションを使用してユーザーモデルを作成したい
```

#### 2. 最新のコード例取得

```text
use context7

Pytestで非同期テストを書く方法は？
```

#### 3. API仕様の確認

```text
use context7

FastAPIのdependency injectionの最新の使い方を教えて
```

## トラブルシューティング

### MCPサーバーが起動しない場合

1. Node.jsバージョンを確認：

   ```bash
   node --version  # 18以上であることを確認
   ```

2. 手動でパッケージを確認：

   ```bash
   npx @upstash/context7-mcp@latest --help
   ```

3. 代替ランタイムを試す：

   ```bash
   # Bunを使用
   bunx @upstash/context7-mcp@latest
   
   # Denoを使用
   deno run --allow-net npm:@upstash/context7-mcp
   ```

### パッケージ解決に失敗する場合

`@latest`を削除して試してください：

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### Context7が動作しない場合

1. MCP対応クライアントで設定を確認
2. クライアントを再起動
3. MCP設定ファイルの形式が正しいか確認

## セキュリティに関する注意事項

- Context7はインターネット接続が必要（最新ドキュメントの取得のため）
- 外部サーバーからドキュメントを取得するため、ネットワークポリシーを確認
- 企業環境ではプロキシ設定が必要な場合があります

## 対応ライブラリ

Context7は以下のような主要ライブラリに対応：

- **Python**: FastAPI、Django、Flask、Pandas、NumPy等
- **JavaScript/TypeScript**: React、Vue、Node.js、Express等
- **その他**: 多くのオープンソースライブラリに対応

## 参考リンク

- [Context7 MCP公式ドキュメント](https://apidog.com/blog/context7-mcp-server/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [@upstash/context7-mcp NPMパッケージ](https://www.npmjs.com/package/@upstash/context7-mcp)
