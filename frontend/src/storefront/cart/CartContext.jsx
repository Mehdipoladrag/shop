import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { cartApi } from "../api/endpoints";

const EMPTY_CART = { items: [], total_count: 0, total_price: 0 };

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [cart, setCart] = useState(EMPTY_CART);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    cartApi
      .get()
      .then(setCart)
      .catch(() => setCart(EMPTY_CART))
      .finally(() => setLoaded(true));
  }, []);

  // Every cart action returns the updated cart, which replaces the local copy.
  const addItem = useCallback((productId, count = 1) => cartApi.add(productId, count).then(setCart), []);
  const setItemCount = useCallback((productId, count) => cartApi.setCount(productId, count).then(setCart), []);
  const removeItem = useCallback((productId) => cartApi.remove(productId).then(setCart), []);

  const value = useMemo(
    () => ({ cart, loaded, addItem, setItemCount, removeItem }),
    [cart, loaded, addItem, setItemCount, removeItem]
  );
  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error("useCart must be used inside CartProvider");
  return context;
}
