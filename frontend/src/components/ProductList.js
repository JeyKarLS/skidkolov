import React from 'react';
import useStore from '../store';
import ProductCard from './ProductCard';

const ProductList = () => {
  const { products, isLoading, error } = useStore();

  if (isLoading) return <p>Загрузка...</p>;
  if (error) return <p>Ошибка: {error}</p>;

  return (
    <div className="product-list">
      {products.length === 0 ? (
        <p>Нет товаров</p>
      ) : (
        products.map(product => (
          <ProductCard key={product.id} product={product} />
        ))
      )}
    </div>
  );
};

export default ProductList;