import React from 'react';
import useStore from '../store';

const ProductCard = ({ product }) => {
  const { user, addToFavorites, removeFromFavorites, favorites } = useStore();
  const isFavorite = favorites.some(fav => fav.product_id === product.id);

  const handleFavorite = () => {
    if (!user) return;
    if (isFavorite) {
      removeFromFavorites(product.id, user.telegram_id);
    } else {
      addToFavorites(product.id, user.telegram_id);
    }
  };

  const handleBuy = () => {
    window.open(product.partner_url, '_blank');
  };

  return (
    <div className="product-card">
      <img src={product.image_url || 'placeholder.jpg'} alt={product.name} />
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <p>Цена: {product.price}₽ {product.old_price && <span>Было: {product.old_price}₽</span>}</p>
      {product.discount && <p>Скидка: {product.discount}%</p>}
      <p>Рейтинг: {product.rating || 'N/A'}</p>
      <button onClick={handleBuy}>Купить с кэшбэком</button>
      {user && (
        <button onClick={handleFavorite}>
          {isFavorite ? 'Убрать из избранного' : 'Добавить в избранное'}
        </button>
      )}
    </div>
  );
};

export default ProductCard;