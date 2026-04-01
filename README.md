# 🏠 Real Estate Platform with House Price Prediction

A full-stack, AI-powered real estate web application built with **Django** and **Machine Learning**. The platform connects property buyers, sellers, and brokers — with a built-in ML engine that predicts fair market prices in real time.

> **MCA Major Project** — Kristu Jyoti College of Management and Technology

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Environment Configuration](#-environment-configuration)
- [Running the Project](#-running-the-project)
- [User Roles](#-user-roles)
- [Machine Learning Module](#-machine-learning-module)
- [Security](#-security)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## 🔍 Overview

The **Real Estate Platform with House Price Prediction** is a multi-role web application that streamlines the end-to-end property transaction lifecycle:

1. **Sellers** list properties with full details and automatically receive an **AI-generated market price estimate**
2. **Buyers** browse, filter, request, and bid on properties
3. **Admin** assigns district-matched **Brokers** to each property request
4. **Buyers and Brokers** communicate through an integrated **chat system**
5. **Admin** monitors platform growth through a **Chart.js Analytics Dashboard**

---

## ✨ Features

### 👤 User (Buyer / Seller)
- Secure registration and login (PBKDF2 SHA256 encrypted passwords)
- OTP-based forgot password via email
- Add and Edit property listings with image upload
- **AI Market Estimate** generated instantly on property save
- Browse properties with **District + Status filters**
- AI Deal Badge on listings: *Amazing Deal / Fair Price / Overvalued*
- Send property purchase requests
- Place bids (one per property, enforced via UI)
- Chat with assigned Broker (unlocks after broker assignment)
- View property location on **interactive Leaflet.js map**

### 🏢 Admin
- **Analytics Dashboard** with 3 Chart.js visualizations:
  - 📈 Monthly Commission Revenue (Line Chart)
  - 🍩 Properties by District (Doughnut Chart)
  - 📊 AI Prediction vs Market Price (Bar Chart)
- Add, Edit, Delete Brokers
- Assign / Replace / Remove Brokers per property
- View all registered users
- View all property requests (paginated)
- View broker commission history

### 🤝 Broker
- View all assigned property requests
- Chat with assigned buyers
- View commission history
- Update profile and change password

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.x, Django 4.2+ |
| **Database** | MySQL (via XAMPP / phpMyAdmin) |
| **Machine Learning** | Scikit-learn, Pandas, NumPy, Pickle |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Charts** | Chart.js |
| **Maps** | Leaflet.js |
| **Icons** | Tabler Icons |
| **Security** | Django PBKDF2 SHA256 hashers, CSRF middleware |
| **Email** | Django SMTP (Gmail) |
| **Version Control** | Git / GitHub |

---

## 📁 Project Structure

```
house/                          ← Django project root
│
├── house/                      ← Core app (login, register, home)
│   ├── models.py               ← All database models
│   ├── view.py                 ← Login, Register, OTP views
│   └── urls.py
│
├── user/                       ← User module
│   ├── views.py                ← Browse, Add, Edit, Bid, Chat views
│   └── urls.py
│
├── broker/                     ← Broker module
│   ├── views.py
│   └── urls.py
│
├── administrator/              ← Admin module
│   ├── views.py                ← Dashboard analytics, Broker management
│   └── urls.py
│
├── ml_engine/                  ← Machine Learning module
│   ├── predictor.py            ← Singleton ML predictor class
│   ├── model.pkl               ← Trained Scikit-learn model
│   └── encoders.pkl            ← Label encoders for categorical features
│
├── templates/                  ← All HTML templates
│   ├── home/                   ← Public homepage
│   ├── login/                  ← Login, Register, OTP pages
│   ├── user/                   ← User dashboard, property, chat
│   ├── broker/                 ← Broker dashboard, chat
│   └── admin/                  ← Admin dashboard, broker mgmt
│
├── media/                      ← Uploaded property images
│   └── property_images/
│
├── static/                     ← Static assets (CSS, JS, images)
│
├── migrate_passwords.py        ← One-time password encryption script
└── manage.py
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or above
- MySQL (XAMPP recommended for Windows)
- pip

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/real-estate-platform.git
cd real-estate-platform/house
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install django mysqlclient scikit-learn pandas numpy pillow
```

### Step 4: Set Up MySQL Database
1. Start **XAMPP** and enable **Apache + MySQL**
2. Open **phpMyAdmin** (`http://localhost/phpmyadmin`)
3. Create a new database called `real_estate_db`
4. Import the provided SQL dump file (if available)

---

## 🔧 Environment Configuration

Open `house/settings.py` and update the following:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'real_estate_db',
        'USER': 'root',
        'PASSWORD': '',          # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Email (for OTP password reset)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'   # Use Gmail App Password

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

> ⚠️ **Important:** Use a Gmail **App Password** (not your regular Gmail password).
> Enable it at: Google Account → Security → 2-Step Verification → App Passwords

---

## ▶️ Running the Project

```bash
# Navigate to the project root
cd house

# Run the development server
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

**Default Admin Login:**
```
URL:      http://127.0.0.1:8000/administrator/dashboardAdmin/
Email:    admin@propertyhub.com
Password: (set in your Login table)
```

---

## 👥 User Roles

| Role | Access URL | Description |
|---|---|---|
| **Public** | `/` | Homepage, property listings |
| **User** | `/user/userDashboard/` | Buyer/Seller dashboard |
| **Broker** | `/broker/dashboardBroker/` | Broker dashboard |
| **Admin** | `/administrator/dashboardAdmin/` | Admin analytics + management |

---

## 🤖 Machine Learning Module

The ML engine uses a **Scikit-learn Random Forest Regressor** trained on property data from Kerala.

**Prediction inputs:**
- `district` — Property district (categorical, label-encoded)
- `location` — Specific location/area (categorical, label-encoded)
- `area` — Property area in square feet (numeric)
- `bedrooms` — Number of bedrooms (numeric)

**How it works:**
1. Model and label encoders are loaded once at startup (`ml_engine/predictor.py`)
2. When a property is added/edited, Django calls the prediction function
3. The predicted price is saved to `price_predicted` in the database
4. Both prices are displayed on the property detail page
5. An admin Chart.js bar chart compares average listed vs AI predicted prices per district

**To retrain the model:**
```bash
cd ml_engine
python train_model.py    # If training script is included
```

---

## 🔐 Security

| Feature | Implementation |
|---|---|
| **Password Hashing** | PBKDF2 SHA256 via `django.contrib.auth.hashers` |
| **CSRF Protection** | Django middleware on all POST forms |
| **SQL Injection** | Django ORM parameterized queries |
| **Session Auth** | `request.session['semail']` checked on every protected view |
| **Role Isolation** | Separate URL namespaces for user/broker/admin |
| **Image Validation** | Server-side check before property save |

> 🔑 **Note:** All passwords are stored as one-way hashes. The original password is **never** stored or recoverable. Password verification uses `check_password()`.

---

## 📸 Screenshots

> *(Add screenshots of your running application here)*

| Page | Description |
|---|---|
| Homepage | Public property listings |
| Admin Dashboard | Chart.js analytics |
| Browse Properties | Filter by district + status |
| Property Detail | AI price estimate |
| Chat Interface | Buyer ↔ Broker messaging |

---

## 🚀 Future Enhancements

- [ ] Mobile application (Android/iOS — React Native)
- [ ] Real-time chat using Django Channels (WebSockets)
- [ ] Email/SMS notifications for new bids and messages
- [ ] Payment gateway integration (Razorpay/Stripe)
- [ ] Property recommendation engine (collaborative filtering)
- [ ] Advanced search (price range slider, area filter)
- [ ] Admin report export (PDF/Excel)
- [ ] Automated ML model retraining pipeline

---

## 👨‍💻 Author

**Alan Varghese**
MCA Student — Kristu Jyoti College of Management and Technology
📧 varghesealan09@gmail.com

---

## 📄 License

This project is developed for academic purposes as part of an MCA Major Project.
All rights reserved © 2026
