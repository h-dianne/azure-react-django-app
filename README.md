# Azure React Django アプリ

React TypeScript フロントエンドと Django バックエンドを使用して Azure Active Directory とのシングルサインオン（SSO）を実装したフルスタックデモアプリケーションです。

## 機能

- **Azure AD SSO 統合**: Microsoft Authentication Library (MSAL) を使用したセキュアな認証
- **React TypeScript フロントエンド**: TypeScript と Tailwind CSS を使用したモダンな React アプリ
- **Django バックエンド**: JWT トークン検証機能付きの Python バックエンド
- **セッション管理**: 自動トークンリフレッシュとセキュアストレージ

## アーキテクチャ

### 認証フロー

- **プロトコル**: OpenID Connect (OIDC) / OAuth 2.0
- **フロー**: セキュリティ強化のための PKCE 付き認証コードフロー
- **トークン管理**: アクセストークンと ID トークンをセッションストレージに保存
- **自動リフレッシュ**: MSAL.js が期限切れ前に自動的にトークンをリフレッシュ

## クイックスタート

### 前提条件

- Node.js（v18 以上）
- Python（v3.11 以上）
- Azure AD アプリケーション登録

### リポジトリのクローン

```bash
git clone https://github.com/h-dianne/azure-react-django-app.git
cd azure-react-django-app
```

### フロントエンドセットアップ

詳細なセットアップ手順については [`frontend/README.md`](frontend/README.md) をご覧ください

```bash
cd frontend
npm install
# .envファイルを設定（frontend/README.md を参照）
npm run dev
```

フロントエンドは `http://localhost:5173` でアクセスできます。

### バックエンドセットアップ

詳細なセットアップ手順については [`backend/README.md`](backend/README.md) をご覧ください

```bash
cd backend
uv sync
# .envファイルを設定（backend/README.md を参照）
uv run python manage.py migrate
uv run python manage.py runserver
```

バックエンド API は `http://localhost:8000` でアクセスできます。

## ドキュメント

- **[フロントエンドドキュメント](frontend/README.md)**: 完全な React TypeScript セットアップと設定
- **[バックエンドドキュメント](backend/README.md)**: 完全な Django バックエンドセットアップとアーキテクチャ

## プロジェクト構造

```text
azure-react-django-app/
├── frontend/                 # React TypeScript フロントエンド
│   ├── src/
│   │   ├── components/      # UI コンポーネント
│   │   ├── config/          # Azure AD 設定
│   │   ├── pages/           # アプリケーションページ
│   │   └── types/           # TypeScript 型定義
│   ├── .env                 # 環境変数
│   ├── package.json         # フロントエンド依存関係
│   └── README.md            # フロントエンドドキュメント
├── backend/                 # Django バックエンド
│   ├── apps/                # Django アプリケーション
│   ├── config/              # Django 設定
│   ├── .env                 # 環境変数
│   ├── pyproject.toml       # バックエンド依存関係
│   └── README.md            # バックエンドドキュメント
└── README.md                # このファイル
```
