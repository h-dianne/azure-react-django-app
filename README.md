# Azure React Django App

A full-stack application implementing Single Sign-On (SSO) with Azure Active Directory using React TypeScript frontend and Django backend.

## Features

- **Azure AD SSO Integration**: Secure authentication using Microsoft Authentication Library (MSAL)
- **React TypeScript Frontend**: Modern React app with TypeScript and Tailwind CSS
- **Django Backend**: Python backend with JWT token verification
- **Session Management**: Automatic token refresh and secure storage

## Architecture

### Authentication Flow

- **Protocol**: OpenID Connect (OIDC) / OAuth 2.0
- **Flow**: Authorization Code Flow with PKCE for enhanced security
- **Token Management**: Access tokens and ID tokens stored in session storage
- **Auto-refresh**: MSAL.js automatically refreshes tokens before expiration

### Frontend Implementation

- **Framework**: React 19 with TypeScript and Vite
- **Authentication Library**: Microsoft Authentication Library (@azure/msal-react, @azure/msal-browser)
- **UI Components**: Custom components with Radix UI and Tailwind CSS
- **Routing**: React Router DOM for navigation
- **Token Storage**: Session storage (not cookies) for better security

### Backend Implementation

- **Framework**: Django with modern Python
- **Token Verification**: PyJWT for access token validation
- **Public Key Caching**: Azure AD public keys cached for 24 hours
- **User Management**: User identification via Azure AD Object ID (oid)
- **Auto User Creation**: Creates new users or denies access based on oid

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.11 or higher)
- Azure AD application registration

### Clone the Repository

```bash
git clone https://github.com/h-dianne/azure-react-django-app.git
cd azure-react-django-app
```

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Configure environment variables:**

   Create a `.env` file in the frontend directory with your Azure AD configuration:

   ```properties
   VITE_CLIENT_ID=your-azure-ad-client-id
   VITE_AUTHORITY=https://login.microsoftonline.com/your-tenant-id
   VITE_REDIRECT_URI=http://localhost:5173/
   VITE_SCOPES=api://your-client-id/access_as_user
   VITE_API_BASE_URL=http://localhost:8000/
   ```

4. **Start the development server:**

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

### Frontend Commands

- **Development server**: `npm run dev`
- **Build for production**: `npm run build`
- **Preview production build**: `npm run preview`
- **Lint code**: `npm run lint`

### Backend Setup

Coming soon...

## Project Structure

```text
azure-react-django-app/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── config/          # Azure AD configuration
│   │   ├── pages/           # Application pages
│   │   └── types/           # TypeScript type definitions
│   ├── .env                 # Environment variables
│   └── package.json         # Frontend dependencies
├── backend/                 # Django backend
│   ├── apps/                # Django applications
│   ├── config/              # Django configuration
│   └── pyproject.toml       # Backend dependencies
└── README.md
```

## Environment Configuration

### Frontend Environment Variables

| Variable            | Description                    | Example                                       |
| ------------------- | ------------------------------ | --------------------------------------------- |
| `VITE_CLIENT_ID`    | Azure AD application client ID | `b579ca6d-274d-4c41-8cf3-7efaaf54da58`        |
| `VITE_AUTHORITY`    | Azure AD tenant authority URL  | `https://login.microsoftonline.com/tenant-id` |
| `VITE_REDIRECT_URI` | OAuth redirect URI             | `http://localhost:5173/`                      |
| `VITE_SCOPES`       | API scopes for token requests  | `api://client-id/access_as_user`              |
| `VITE_API_BASE_URL` | Backend API base URL           | `http://localhost:8000/`                      |
