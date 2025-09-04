import type { Configuration, PopupRequest } from "@azure/msal-browser";

// Configuration object for MSAL instance
// Contains authentication settings and cache configuration for Azure AD integration
// All auth values are loaded from environment variables to support different environments
export const msalConfig: Configuration = {
  auth: {
    clientId: import.meta.env.VITE_CLIENT_ID, // Azure AD app registration client ID
    authority: import.meta.env.VITE_AUTHORITY, // Azure AD tenant authority URL
    redirectUri: import.meta.env.VITE_REDIRECT_URI // URL to redirect after authentication
  },
  cache: {
    cacheLocation: "sessionStorage", // Store tokens in browser session storage
    storeAuthStateInCookie: false // Don't use cookies for auth state (modern browsers)
  }
};

// Login request configuration for MSAL authentication
// Defines the OAuth scopes (permissions) that the app will request during login
// The scopes are loaded from the VITE_SCOPES environment variable at build time
// Note: This creates an array with a single string element - if multiple scopes are needed,
// consider splitting the environment variable string (e.g., VITE_SCOPES.split(' '))
export const loginRequest: PopupRequest = {
  scopes: [import.meta.env.VITE_SCOPES]
};
