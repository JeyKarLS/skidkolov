<<<<<<< HEAD
# СкидкоЛов - Telegram Mini App + Bot

Полнофункциональный продукт для поиска скидок и кэшбэка в Telegram.

## 🚀 Функции

- **Mini App**: Поиск товаров, фильтры, избранное
- **Telegram Bot**: Уведомления, управление подпиской
- **Backend**: FastAPI с PostgreSQL
- **Монетизация**: Партнерские ссылки, подписки, реклама

## 🛠️ Технологии

- **Frontend**: React + Zustand + Axios
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Bot**: aiogram 3.x
- **Deploy**: Vercel (frontend) + Railway (backend)

## 📦 Установка

### Локальная разработка

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/your-username/skidkolov.git
   cd skidkolov
   ```

2. **Backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python add_sample_products.py
   uvicorn main:app --reload
   ```

3. **Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Bot**
   ```bash
   cd bot
   python -m venv venv
   venv\Scripts\activate
   pip install aiogram httpx
   python main.py
   ```

## 🚀 Развертывание

### Автоматическое (рекомендуется)

1. **Создайте GitHub репозиторий** и запушьте код
2. **Frontend на Vercel**:
   - Подключите GitHub
   - Выберите папку `frontend`
   - Build settings: `npm run build`, `build`
3. **Backend на Railway**:
   - Подключите GitHub
   - Выберите папку `backend`
   - Переменные: `DATABASE_URL` (авто от Railway)

### Ручное развертывание

См. инструкции в коде для Vercel CLI и Railway CLI.

## ⚙️ Настройка

1. **Bot Token**: Получите у [@BotFather](https://t.me/botfather)
2. **Web App**: Настройте в BotFather `/setmenubutton`
3. **База данных**: Railway предоставит PostgreSQL автоматически

## 📱 Использование

1. Откройте бота в Telegram
2. Нажмите "Открыть СкидкоЛов"
3. Ищите товары, добавляйте в избранное
4. Получайте уведомления о скидках

## 📊 API

### Backend Endpoints

- `GET /products` - Список товаров
- `POST /users/auth` - Аутентификация
- `GET /favorites?telegram_id=123` - Избранное
- `POST /favorites/{product_id}` - Добавить в избранное

## 🤝 Вклад

1. Fork репозиторий
2. Создайте feature branch
3. Commit изменения
4. Push и создайте Pull Request

## 📄 Лицензия

MIT License

## 📞 Контакты

Email: alekscesnokov5@gmail.com
