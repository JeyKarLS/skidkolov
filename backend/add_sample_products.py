import asyncio
from database import async_session, engine
from models import Product
from sqlalchemy.future import select

async def add_sample_products():
    async with async_session() as session:
        # Check if products exist
        result = await session.execute(select(Product).limit(1))
        if result.scalar_one_or_none():
            print("Products already exist")
            return
        
        sample_products = [
            {
                "name": "iPhone 15 Pro",
                "description": "Новый флагман Apple",
                "price": 99999,
                "old_price": 119999,
                "discount": 17,
                "image_url": "https://example.com/iphone.jpg",
                "product_url": "https://ozon.ru/product/iphone-15",
                "partner_url": "https://ozon.ru/partner?product=iphone-15",
                "rating": 4.8,
                "category": "electronics",
                "shop": "Ozon"
            },
            {
                "name": "Nike Air Max",
                "description": "Удобные кроссовки для бега",
                "price": 12999,
                "old_price": 15999,
                "discount": 19,
                "image_url": "https://example.com/nike.jpg",
                "product_url": "https://wildberries.ru/product/nike-air-max",
                "partner_url": "https://wildberries.ru/partner?product=nike-air-max",
                "rating": 4.5,
                "category": "shoes",
                "shop": "Wildberries"
            }
            # Add more as needed
        ]
        
        for prod_data in sample_products:
            product = Product(**prod_data)
            session.add(product)
        
        await session.commit()
        print("Sample products added")

if __name__ == "__main__":
    asyncio.run(add_sample_products())