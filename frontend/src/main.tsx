import { createRoot } from "react-dom/client";
import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";
import { msalConfig } from "./config/authConfig";
import { App } from "./App";
import "./styles/index.css";

const msalInstance = new PublicClientApplication(msalConfig);

const container = document.getElementById("root");
const root = createRoot(container!);

// console.log("msalConfig", msalConfig);
// console.log("loginRequest", loginRequest);

root.render(
  <MsalProvider instance={msalInstance}>
    <App />
  </MsalProvider>
);
