# フロントエンド - Azure AD SSO を使った React TypeScript

Azure Active Directory のシングルサインオン統合を持つモダンな React TypeScript フロントエンドアプリケーションです。

## 機能

- **Azure AD 統合**: Microsoft Authentication Library (MSAL) を使用したシームレスな SSO
- **モダンな React**: 高速開発のための React 19 と TypeScript、Vite
- **UI コンポーネント**: Radix UI と Tailwind CSS で構築されたカスタムコンポーネント
- **ルーティング**: React Router DOM によるクライアントサイドルーティング
- **セキュアなトークン管理**: 自動リフレッシュ付きの JWT トークンのセッションストレージ

## 技術スタック

- **フレームワーク**: TypeScript を使った React 19
- **ビルドツール**: 高速開発とビルドのための Vite
- **認証**: Microsoft Authentication Library (@azure/msal-react, @azure/msal-browser)
- **UI フレームワーク**: カスタムコンポーネント付きの Tailwind CSS
- **コンポーネントライブラリ**: Radix UI プリミティブ
- **HTTP クライアント**: API 通信のための Axios
- **ルーティング**: React Router DOM

## 実装詳細

### 認証フロー

- **プロトコル**: OpenID Connect (OIDC) / OAuth 2.0
- **フロー**: セキュリティ強化のための PKCE 付き認証コードフロー
- **トークンストレージ**: セキュリティ向上のためのセッションストレージ
- **自動リフレッシュ**: MSAL.js が期限切れ前に自動的にトークンをリフレッシュ

### 主要コンポーネント

- **MSAL 設定**: `src/config/authConfig.ts` での Azure AD 設定
- **認証ページ**: ログイン、ダッシュボード、ログアウトコンポーネント
- **保護されたルート**: ルートレベルの認証ガード
- **トークン管理**: 自動トークン取得とリフレッシュ

## セットアップ

### 前提条件

- Node.js（v18 以上）
- Azure AD アプリケーション登録

### インストール

1. **依存関係をインストール:**

   ```bash
   npm install
   ```

2. **環境変数を設定:**

   frontend ディレクトリに `.env` ファイルを作成:

   ```properties
   VITE_CLIENT_ID=your-azure-ad-client-id
   VITE_AUTHORITY=https://login.microsoftonline.com/your-tenant-id
   VITE_REDIRECT_URI=http://localhost:5173/
   VITE_SCOPES=api://your-client-id/access_as_user
   VITE_API_BASE_URL=http://localhost:8000/
   ```

3. **開発サーバーを起動:**

   ```bash
   npm run dev
   ```

   アプリケーションは `http://localhost:5173` で利用できます

## 利用可能なスクリプト

- **`npm run dev`**: ホットリロード付き開発サーバーを開始
- **`npm run build`**: 本番用アプリケーションをビルド
- **`npm run preview`**: 本番ビルドをローカルでプレビュー
- **`npm run lint`**: コード品質チェックのため ESLint を実行

## 環境変数

| 変数名              | 説明                                     | 例                                            |
| ------------------- | ---------------------------------------- | --------------------------------------------- |
| `VITE_CLIENT_ID`    | Azure AD アプリケーションクライアント ID | `your-client-id`                              |
| `VITE_AUTHORITY`    | Azure AD テナント認証局 URL              | `https://login.microsoftonline.com/tenant-id` |
| `VITE_REDIRECT_URI` | OAuth リダイレクト URI                   | `http://localhost:5173/`                      |
| `VITE_SCOPES`       | トークンリクエスト用 API スコープ        | `api://client-id/access_as_user`              |
| `VITE_API_BASE_URL` | バックエンド API ベース URL              | `http://localhost:8000/`                      |

## プロジェクト構造

```text
frontend/
├── src/
│   ├── components/         # 再利用可能な UI コンポーネント
│   │   ├── auth/           # 認証関連コンポーネント
│   │   ├── layout/         # レイアウトコンポーネント
│   │   └── ui/             # ベース UI コンポーネント（ボタン、カードなど）
│   ├── config/
│   │   └── authConfig.ts   # Azure AD MSAL 設定
│   ├── hooks/              # カスタム React フック
│   ├── lib/
│   │   └── utils.ts        # ユーティリティ関数
│   ├── pages/              # アプリケーションページ
│   │   ├── Dashboard.tsx   # 保護されたダッシュボードページ
│   │   ├── Login.tsx       # ログインページ
│   │   └── Logout.tsx      # ログアウトページ
│   ├── styles/
│   │   └── index.css       # グローバルスタイルと Tailwind インポート
│   ├── types/
│   │   └── index.ts        # TypeScript 型定義
│   ├── App.tsx             # メインアプリケーションコンポーネント
│   └── main.tsx            # アプリケーションエントリーポイント
├── .env                    # 環境変数（これを作成）
├── package.json            # 依存関係とスクリプト
├── vite.config.ts          # Vite 設定
└── tsconfig.json           # TypeScript 設定
```

## Azure AD 設定

### 必要な Azure AD セットアップ

1. **アプリ登録**: Azure AD アプリ登録を作成
2. **リダイレクト URI**: `http://localhost:5173/`（と本番 URL）を追加
3. **API アクセス許可**: 必要なスコープを設定
4. **トークン設定**: 暗黙的フロー用の ID トークンを有効化

### MSAL 設定

MSAL 設定は `src/config/authConfig.ts` で一元化されています:

```typescript
export const msalConfig: Configuration = {
  auth: {
    clientId: import.meta.env.VITE_CLIENT_ID,
    authority: import.meta.env.VITE_AUTHORITY,
    redirectUri: import.meta.env.VITE_REDIRECT_URI
  },
  cache: {
    cacheLocation: "sessionStorage",
    storeAuthStateInCookie: false
  }
};
```
