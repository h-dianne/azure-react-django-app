# Frontend - React TypeScript with Azure AD SSO

A modern React TypeScript frontend application with Azure Active Directory Single Sign-On integration.

## Features

- **Azure AD Integration**: Seamless SSO using Microsoft Authentication Library (MSAL)
- **Modern React**: React 19 with TypeScript and Vite for fast development
- **UI Components**: Custom components built with Radix UI and Tailwind CSS
- **Routing**: Client-side routing with React Router DOM
- **Secure Token Management**: Session storage for JWT tokens with automatic refresh

## Technology Stack

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite for fast development and building
- **Authentication**: Microsoft Authentication Library (@azure/msal-react, @azure/msal-browser)
- **UI Framework**: Tailwind CSS with custom components
- **Component Library**: Radix UI primitives
- **HTTP Client**: Axios for API communication
- **Routing**: React Router DOM

## Implementation Details

### Authentication Flow

- **Protocol**: OpenID Connect (OIDC) / OAuth 2.0
- **Flow**: Authorization Code Flow with PKCE for enhanced security
- **Token Storage**: Session storage (not cookies) for better security
- **Auto-refresh**: MSAL.js automatically refreshes tokens before expiration

### Key Components

- **MSAL Configuration**: Centralized Azure AD configuration in `src/config/authConfig.ts`
- **Authentication Pages**: Login, Dashboard, and Logout components
- **Protected Routes**: Route-level authentication guards
- **Token Management**: Automatic token acquisition and refresh

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Azure AD application registration

### Installation

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Configure environment variables:**

   Create a `.env` file in the frontend directory:

   ```properties
   VITE_CLIENT_ID=your-azure-ad-client-id
   VITE_AUTHORITY=https://login.microsoftonline.com/your-tenant-id
   VITE_REDIRECT_URI=http://localhost:5173/
   VITE_SCOPES=api://your-client-id/access_as_user
   VITE_API_BASE_URL=http://localhost:8000/
   ```

3. **Start the development server:**

   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

## Available Scripts

- **`npm run dev`**: Start development server with hot reload
- **`npm run build`**: Build the application for production
- **`npm run preview`**: Preview the production build locally
- **`npm run lint`**: Run ESLint to check code quality

## Environment Variables

| Variable            | Description                    | Example                                       |
| ------------------- | ------------------------------ | --------------------------------------------- |
| `VITE_CLIENT_ID`    | Azure AD application client ID | `your-client-id`                              |
| `VITE_AUTHORITY`    | Azure AD tenant authority URL  | `https://login.microsoftonline.com/tenant-id` |
| `VITE_REDIRECT_URI` | OAuth redirect URI             | `http://localhost:5173/`                      |
| `VITE_SCOPES`       | API scopes for token requests  | `api://client-id/access_as_user`              |
| `VITE_API_BASE_URL` | Backend API base URL           | `http://localhost:8000/`                      |

## Project Structure

```text
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── auth/           # Authentication-related components
│   │   ├── layout/         # Layout components
│   │   └── ui/             # Base UI components (buttons, cards, etc.)
│   ├── config/
│   │   └── authConfig.ts   # Azure AD MSAL configuration
│   ├── hooks/              # Custom React hooks
│   ├── lib/
│   │   └── utils.ts        # Utility functions
│   ├── pages/              # Application pages
│   │   ├── Dashboard.tsx   # Protected dashboard page
│   │   ├── Login.tsx       # Login page
│   │   └── Logout.tsx      # Logout page
│   ├── styles/
│   │   └── index.css       # Global styles and Tailwind imports
│   ├── types/
│   │   └── index.ts        # TypeScript type definitions
│   ├── App.tsx             # Main application component
│   └── main.tsx            # Application entry point
├── .env                    # Environment variables (create this)
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite configuration
└── tsconfig.json           # TypeScript configuration
```

## Azure AD Configuration

### Required Azure AD Setup

1. **App Registration**: Create an Azure AD app registration
2. **Redirect URIs**: Add `http://localhost:5173/` (and production URLs)
3. **API Permissions**: Configure necessary scopes
4. **Token Configuration**: Enable ID tokens for implicit flow

### MSAL Configuration

The MSAL configuration is centralized in `src/config/authConfig.ts`:

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
