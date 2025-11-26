# Payments API Microservice

Микросервис для централизованной работы с балансом пользователей: зачисление, списание, перевод средств и получение текущего баланса. Сервис предоставляет HTTP API и работает с PostgreSQL (основная БД) и Redis (кэширование, при необходимости).

---

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/tt0add/payments-api.git
cd payments-api
```

2. Запустите через docker compose:

```bash
docker compose up
```
---
🚀 **Стек технологий**

🐍 **Python 3.11+**  
⚡ **FastAPI**  
🗄️ **SQLAlchemy**  
🐘 **PostgreSQL**  
🧠 **Redis**  
🐳 **Docker + Docker Compose**

---
🧩 API Методы:

➕ Пополнение баланса
```bash
curl -X POST "http://localhost:8000/payments/add" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "sum": 1000}'
```
---
➖ Списание средств
```bash
curl -X POST "http://localhost:8000/payments/remove" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "sum": 500}'
```
---
🔁 Перевод от юзера к юзеру
```bash
curl -X POST "http://localhost:8000/payments/transfer" \
     -H "Content-Type: application/json" \
     -d '{"user1_id": 1, "user2_id": 2, "sum": 300}'
```
---
💰 Получить баланс
```bash
curl -X GET "http://localhost:8000/users/1/balance"
```
С валютой:
```bash
curl -X GET "http://localhost:8000/users/1/balance?currency=USD"
```
---
🧾 Получить транзакции
```bash
curl -X GET "http://localhost:8000/users/1/transactions"
```