import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { CartProvider } from "./cart/CartContext";
import { AuthProvider } from "./auth/AuthContext";
import { FlashProvider } from "./components/Flash";
import "./styles/app.css";
import App from "./App";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <FlashProvider>
            <App />
          </FlashProvider>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
