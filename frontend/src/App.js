import React, { useEffect } from 'react';
import useStore from './store';
import ProductList from './components/ProductList';
import './App.css';

function App() {
  const { user, authenticateUser, fetchProducts, fetchFavorites } = useStore();

  useEffect(() => {
    // For local testing, mock Telegram WebApp
    const WebApp = window.Telegram?.WebApp || { initData: 'test', ready: () => console.log('WebApp ready') };
    WebApp.ready();
    const initData = WebApp.initData;
    if (initData) {
      authenticateUser(initData);
    }
    fetchProducts();
  }, [authenticateUser, fetchProducts]);

  useEffect(() => {
    if (user) {
      fetchFavorites(user.telegram_id);
    }
  }, [user, fetchFavorites]);

  return (
    <div className="App">
      <header>
        <h1>СкидкоЛов</h1>
        {user && <p>Привет, {user.first_name}!</p>}
      </header>
      <main>
        <ProductList />
      </main>
    </div>
  );
}

export default App;
