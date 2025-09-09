# Azure React Django App

A full-stack demo application implementing Single Sign-On (SSO) with Azure Active Directory using React TypeScript frontend and Django backend.

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

## Quick Start

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

See detailed setup instructions in [`frontend/README.md`](frontend/README.md)

```bash
cd frontend
npm install
# Configure .env file (see frontend/README.md)
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Backend Setup

See detailed setup instructions in [`backend/README.md`](backend/README.md)

```bash
cd backend
uv sync
# Configure .env file (see backend/README.md)
uv run python manage.py migrate
uv run python manage.py runserver
```

Backend API will be available at `http://localhost:8000`

## Documentation

- **[Frontend Documentation](frontend/README.md)**: Complete React TypeScript setup and configuration
- **[Backend Documentation](backend/README.md)**: Complete Django backend setup and architecture

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
│   ├── package.json         # Frontend dependencies
│   └── README.md            # Frontend documentation
├── backend/                 # Django backend
│   ├── apps/                # Django applications
│   ├── config/              # Django configuration
│   ├── .env                 # Environment variables
│   ├── pyproject.toml       # Backend dependencies
│   └── README.md            # Backend documentation
└── README.md                # This file
```
