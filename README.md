# TradeFlow - Virtual Stock Market Simulator

A Django-based stock market simulation game with statistically-driven price movements (no external APIs).

## 📁 Project Structure

```
tradeflow/
├── manage.py
├── requirements.txt
├── tradeflow/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── market/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── utils.py
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           ├── update_prices.py
│           └── seed_stocks.py
├── game/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── market.html
    ├── leaderboard.html
    └── transactions.html
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Database Tables

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User

```bash
python manage.py createsuperuser
```

### 4. Seed Initial Stock Data

```bash
python manage.py seed_stocks
```

This creates 5 stocks:
- RF1 (ReelFlow Industries) - ¥120.00
- OCN (OceanTech) - ¥85.00
- NKT (Nakata Motors) - ¥150.00
- TXI (TechnoXi Corp) - ¥95.50
- BST (BioStar Pharma) - ¥210.00

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## 🎮 Game Features

- **¥1,000,000 starting balance** for each new player
- **Buy/Sell stocks** with real-time simulated prices
- **Portfolio tracking** with dashboard analytics
- **Transaction history** for all trades
- **Leaderboard** ranking by total portfolio value
- **Price simulation** using Geometric Brownian Motion

## 📊 Price Simulation

Prices update via GBM formula:
```
S(t+1) = S(t) × exp((μ - σ²/2) + σ × ε)
```

Update prices manually:
```bash
python manage.py update_prices
```

Or via Django admin: Select stocks → "Update Prices Now"

## 🔧 Admin Access

Access admin panel at: http://127.0.0.1:8000/admin

Features:
- Manage users and balances
- Add/edit stocks
- View all transactions
- Update prices with one click

## 🎯 Usage

1. **Register** a new account
2. **Browse** available stocks in the Market
3. **Buy** stocks when prices are low
4. **Sell** when prices rise
5. **Track** your portfolio on the Dashboard
6. **Compete** on the Leaderboard

## 🔄 Scheduled Price Updates

For production, add to crontab:
```bash
*/5 * * * * cd /path/to/tradeflow && python manage.py update_prices
```

This updates prices every 5 minutes.

## 📝 Notes

- Uses SQLite by default (easy setup)
- No external APIs required
- All prices are mathematically simulated
- Safe learning environment (virtual money only)
- Bootstrap 5 + Chart.js for UI

## 🛠️ Customization

Edit stock parameters in admin:
- **Volatility** (σ): Higher = more price swings
- **Drift** (μ): Positive = upward trend

Add more stocks via admin or `seed_stocks.py`