import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import App from "./App";
import { installFonts } from "../shared/fonts";
import "../shared/palette.css";
import "../shared/fonts.css";
import "./styles/base.css";
import "./styles/layout.css";
import "./styles/components.css";

installFonts();

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter basename="/panel">
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
