
---

### 📌 **README.md for Apartment Rental**  

```md
# 🏠 Apartment Rental Manager

Apartment Rental Manager is a Django-based web application designed to help landlords efficiently manage tenants, rental payments, and property details. The system provides authentication, calendar-based tracking, and a user-friendly dashboard.

---

## 📌 Project Features
- 🔐 **User Authentication** (Registration, Login, Profile Update, Password Change)
- 🏢 **Tenant Management** (Track tenants and lease agreements)
- 📅 **Calendar Integration** (Monitor apartment availability)
- 💰 **Payment Tracking** (Record rental payments)
- 📊 **Dashboard** (Insights & analytics)

---

## 🚀 Getting Started

### 📂 Clone the Repository
```bash
git clone https://github.com/Shafiul-Sabbir/apartment_rental.git
cd apartment_rental/rental
```

### 🛠️ Set Up Virtual Environment

- **Windows (CMD/PowerShell)**
  ```powershell
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS/Linux (Terminal)**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔄 Apply Migrations
```bash
python manage.py migrate
```

### 🔑 Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```
Follow the prompts to set up your admin credentials.

### 🚀 Run the Development Server
```bash
python manage.py runserver
```
Access the project at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
Test the Login credentials : (id : admin, pass : admin)

---

## 🔧 Environment Variables (.env)
Create a `.env` file inside the **rental** directory and add:
```ini
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=your_database_url_here
```
*(Replace `your_secret_key_here` with your actual Django secret key.)*

---

## 🎨 Managing Static Files
If static files are not loading properly, run:
```bash
python manage.py collectstatic --noinput
```

---

## 🏗 Project Structure
```
apartment_rental/
│── authentication/      # User authentication system
│── calendar_app/        # Calendar for tenant tracking
│── rental/              # Core Django project files
│── tenants/             # Tenant management module
│── static/              # CSS, JavaScript, and images
│── templates/           # HTML templates
│── manage.py            # Django CLI management tool
│── requirements.txt     # Project dependencies
│── README.md            # This file
```

---

## ✅ Additional Commands
- 📌 **Run Tests:**  
  ```bash
  python manage.py test
  ```
- 🔄 **Reset Migrations (If needed):**  
  ```bash
  find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
  python manage.py makemigrations
  python manage.py migrate
  ```

---

## 📌 Built With
- 🐍 **Django (Python 3.8+)**
- 🗄 **PostgreSQL / SQLite (Database)**
- 🎨 **Bootstrap (Frontend UI)**
- ☁️ **Ready for Deployment on VPS/Cloud**

---

## 🤝 Contribution & Support
📬 **Email:** sabbirvai82@gmail.com  
🌟 **GitHub:** [Shafiul-Sabbir](https://github.com/Shafiul-Sabbir)  

---

🚀 *Happy Coding!* 😊
```

---
