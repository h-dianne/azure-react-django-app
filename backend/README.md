# バックエンド - Azure AD JWT 認証 Django

Azure Active Directory JWT トークン認証を使用した Django REST Framework バックエンドです。

## 機能

- **Azure AD JWT 検証**: PyJWT を使用したセキュアなトークン検証
- **自動ユーザー管理**: Azure AD オブジェクト ID (oid) によるユーザー作成/識別
- **公開キーキャッシュ**: パフォーマンス向上のための Azure AD 公開キーの 24 時間キャッシュ
- **Django REST Framework**: DRF を使用したモダンな API 開発
- **カスタム認証**: シームレスな Azure AD 統合のための DRF 認証クラス

## 技術スタック

- **フレームワーク**: Django REST Framework を使った Django 5.2+
- **パッケージマネージャー**: UV パッケージマネージャー
- **JWT ライブラリ**: トークン検証のための PyJWT
- **暗号化**: Azure AD 公開キーを使用した RSA 署名検証
- **キャッシュ**: 公開キーストレージのための Django Redis キャッシュ
- **HTTP クライアント**: Azure AD API 呼び出しのための Requests ライブラリ

## 実装詳細

### 認証アーキテクチャ

- **JWT トークン検証**: Azure AD 公開キーを使用した RS256 アルゴリズム
- **公開キー管理**: 自動取得と 24 時間キャッシュ
- **ユーザー解決**: トークンクレームからオブジェクト ID (oid) を抽出
- **セキュリティ**: セキュリティ強化のためのオーディエンスとイシュア検証

### 主要コンポーネント

- **`AzureADAuthentication`**: トークン検証を処理する DRF 認証クラス
- **`AzureADJWTService`**: JWT 検証と公開キー管理のサービス
- **`AzureADBackend`**: セッションベース認証用の Django 認証バックエンド
- **カスタムユーザーモデル**: Azure AD オブジェクト ID サポート付き拡張ユーザーモデル

## セットアップ

### 前提条件

- Python（v3.11 以上）
- UV パッケージマネージャー
- Azure AD アプリケーション登録

### インストール

1. **UV をインストール（まだインストールしていない場合）:**

   ```bash
   pip install uv
   ```

2. **依存関係をインストールし、仮想環境を作成:**

   ```bash
   uv sync
   ```

3. **環境変数を設定:**

   backend ディレクトリに `.env` ファイルを作成:

   ```properties
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here

   # Azure AD Configuration
   AZURE_AD_TENANT_ID=your-tenant-id
   AZURE_AD_CLIENT_ID=your-client-id
   AZURE_AD_AUDIENCE=api://your-client-id/access_as_user
   AZURE_AD_ISSUER=https://login.microsoftonline.com/your-tenant-id/v2.0
   AZURE_AD_JWKS_URI=https://login.microsoftonline.com/your-tenant-id/discovery/v2.0/keys
   ```

4. **データベースマイグレーションを実行:**

   ```bash
   uv run python manage.py migrate
   ```

5. **開発サーバーを起動:**

   ```bash
   uv run python manage.py runserver
   ```

   API は `http://localhost:8000` で利用できます

## コマンド

- **`uv run python manage.py migrate`**: データベースマイグレーションを実行
- **`uv run python manage.py makemigrations`**: 新しいマイグレーションを作成
- **`uv run python manage.py createsuperuser`**: 管理者ユーザーを作成
- **`uv run python manage.py test`**: テストスイートを実行
- **`uv run python manage.py shell`**: Django インタラクティブシェル

## 環境変数

| 変数名               | 説明                                     | 例                                                                |
| -------------------- | ---------------------------------------- | ----------------------------------------------------------------- |
| `DEBUG`              | Django デバッグモード                    | `True`                                                            |
| `SECRET_KEY`         | Django シークレットキー                  | `your-secret-key-here`                                            |
| `AZURE_AD_TENANT_ID` | Azure AD テナント ID                     | `your-tenant-id`                                                  |
| `AZURE_AD_CLIENT_ID` | Azure AD アプリケーションクライアント ID | `your-client-id`                                                  |
| `AZURE_AD_AUDIENCE`  | JWT トークンで期待されるオーディエンス   | `api://client-id/access_as_user`                                  |
| `AZURE_AD_ISSUER`    | JWT イシュア URL                         | `https://login.microsoftonline.com/tenant-id/v2.0`                |
| `AZURE_AD_JWKS_URI`  | Azure AD 公開キーエンドポイント          | `https://login.microsoftonline.com/tenant-id/discovery/v2.0/keys` |

## プロジェクト構造

```text
backend/
├── apps/                    # Django アプリケーション
│   ├── authentication/     # Azure AD 認証ロジック
│   │   ├── backends.py     # DRF 認証クラス
│   │   ├── services.py     # JWT 検証サービス
│   │   └── utils.py        # ヘルパーユーティリティ
│   ├── core/               # コアアプリケーションロジック
│   └── users/              # ユーザーモデルと管理
├── config/                 # Django 設定
│   ├── settings/           # 環境固有の設定
│   │   ├── base.py        # ベース設定
│   │   └── development.py  # 開発設定
│   ├── urls.py            # URL 設定
│   └── wsgi.py            # WSGI アプリケーション
├── .env                   # 環境変数（これを作成）
├── manage.py              # Django 管理スクリプト
└── pyproject.toml         # Python 依存関係（UV 形式）
```

## 認証フロー

### JWT トークン検証プロセス

1. **トークン抽出**: Authorization ヘッダーから Bearer トークンを抽出
2. **ヘッダー検証**: トークンヘッダーをデコードしてキー ID (kid) を取得
3. **公開キー取得**: Azure AD 公開キーを取得（24 時間キャッシュ付き）
4. **キーマッチング**: kid を使用して適切な公開キーを検索
5. **トークン検証**: 署名、有効期限、オーディエンス、イシュアを検証
6. **クレーム抽出**: トークンクレームからユーザー情報を抽出
7. **ユーザー解決**: オブジェクト ID (oid) に基づいてユーザーを取得または作成

### セキュリティ機能

- **RS256 アルゴリズム**: セキュアなトークン検証のための非対称暗号
- **オーディエンス検証**: トークンがこのアプリケーション用であることを確認
- **イシュア検証**: トークンが信頼できる Azure AD テナントからのものであることを確認
- **有効期限チェック**: JWT 有効期限クレームを尊重
- **自動キーローテーション**: Azure AD 公開キーの変更をシームレスに処理
- **包括的エラー処理**: 認証失敗に対する適切な HTTP レスポンス

## Azure AD 設定

### 必要な Azure AD セットアップ

1. **アプリ登録**: Azure AD アプリ登録を作成
2. **API アクセス許可**: 必要な API スコープを設定
3. **API の公開**: アプリケーション用のカスタムスコープを作成
4. **認証**: トークン設定とリダイレクト URI を設定

### トークンクレーム

バックエンドは JWT トークンに以下のクレームを期待します:

- **`aud`**: オーディエンス（AZURE_AD_AUDIENCE と一致する必要があります）
- **`iss`**: イシュア（AZURE_AD_ISSUER と一致する必要があります）
- **`oid`**: オブジェクト ID（ユーザー識別に使用）
- **`exp`**: 有効期限
- **`sub`**: サブジェクト識別子

## API エンドポイント

### 認証

すべての API エンドポイントには、Authorization ヘッダーに有効な Azure AD JWT トークンが必要です:

```text
Authorization: Bearer <your-jwt-token>
```

### 保護されたエンドポイントの例

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.authentication.backends import AzureADAuthentication

@api_view(['GET'])
def protected_view(request):
    # 認証は DRF によって自動的に処理されます
    user = request.user  # 認証された Azure AD ユーザー
    return Response({'message': f'Hello, {user.username}!'})
```

## キャッシュ

バックエンドは Azure AD 公開キーのためのインテリジェントキャッシュを実装しています:

- **キャッシュ期間**: 24 時間（設定可能）
- **キャッシュキー**: `azure_ad_jwks`
- **フォールバック**: キャッシュミス時の自動再取得
- **パフォーマンス**: Azure AD への API 呼び出しを削減

## エラー処理

### 認証エラー

- **`401 Unauthorized`**: 無効または期限切れのトークン
- **`403 Forbidden`**: 有効なトークンですが権限不足
- **HTTP ヘッダー**: 401 レスポンス用の適切な WWW-Authenticate ヘッダー
