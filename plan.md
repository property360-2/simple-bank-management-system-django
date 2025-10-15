## 🏦 **Simple Bank Management System – Project Plan**

### 🎯 **Goal**

Create a simple, modular, and reusable web app for managing:

- Customers
- Accounts
- Transactions

---

## ⚙️ **1. Tech Stack**

| Layer                  | Choice                               | Reason                                         |
| ---------------------- | ------------------------------------ | ---------------------------------------------- |
| **Backend Language**   | **Python 3**                         | Stable, widely used, clean syntax              |
| **Web Framework**      | **Django 5**                         | Built-in ORM, authentication, templates, admin |
| **Database**           | **SQLite (dev)** → PostgreSQL (prod) | Simple for dev, scalable later                 |
| **Frontend Framework** | **Bootstrap 5**                      | Quick, responsive, easy to reuse               |
| **Template Engine**    | **Django Templates**                 | Simple and integrated                          |
| **API (optional)**     | **Django REST Framework (DRF)**      | For mobile/app integration                     |
| **Version Control**    | **Git + GitHub**                     | Collaboration & versioning                     |
| **Environment**        | **Virtualenv / venv**                | Isolated dependencies                          |

---

## 📦 **2. Main Django Apps (Modular Design)**

| App              | Purpose                                      | Notes                       |
| ---------------- | -------------------------------------------- | --------------------------- |
| **users**        | Handle login, registration, profiles         | Custom user model           |
| **accounts**     | Manage accounts (balance, type)              | CRUD operations             |
| **transactions** | Deposits, withdrawals, transfers             | Record keeping + validation |
| **core**         | Shared logic (base templates, mixins, utils) | Reusability layer           |
| **dashboard**    | Summary & analytics                          | Optional (later phase)      |

---

## 🎨 **3. Frontend Libraries**

| Library                  | Use                                    |
| ------------------------ | -------------------------------------- |
| **Bootstrap 5**          | Responsive layout & components         |
| **Font Awesome**         | Icons (e.g., money, user, transaction) |
| **Alpine.js** (optional) | Light interactivity (modals, toggle)   |
| **Chart.js** (optional)  | Dashboard graphs                       |

---

## 🧩 **4. Reusable Frontend Components**

| Component              | Description                            | Used In                    |
| ---------------------- | -------------------------------------- | -------------------------- |
| **`_navbar.html`**     | Top navigation bar                     | Every page                 |
| **`_alerts.html`**     | Shows Django messages (success, error) | All forms/views            |
| **`_form.html`**       | Generic form renderer                  | Create/Edit views          |
| **`_table.html`**      | Reusable data table                    | Account list, transactions |
| **`_modal.html`**      | Confirm dialogs (e.g., delete)         | CRUD actions               |
| **`_pagination.html`** | Page navigation                        | Account/Transaction lists  |

These are stored under:

```
templates/includes/
```

---

## 🧱 **5. Database Models (Simplified)**

| Model           | Fields                                 | Purpose                  |
| --------------- | -------------------------------------- | ------------------------ |
| **User**        | username, email, phone                 | Custom user profile      |
| **Account**     | user, account_type, balance            | Each user’s bank account |
| **Transaction** | from_account, to_account, amount, type | Money movement record    |

---

## 🧮 **6. Basic Features (MVP)**

| Module                   | Features                                   |
| ------------------------ | ------------------------------------------ |
| **Auth**                 | Login / Logout / Register                  |
| **Account Management**   | View, create, edit, delete accounts        |
| **Transactions**         | Deposit, withdraw, transfer                |
| **Dashboard (optional)** | Display total balance, recent transactions |

---

## 🧰 **7. Tools and Setup**

| Tool                  | Use                        |
| --------------------- | -------------------------- |
| **VS Code / PyCharm** | IDE                        |
| **Postman**           | API testing (if DRF added) |
| **GitHub**            | Code repo                  |
| **venv**              | Virtual environment        |
| **pytest / unittest** | Testing                    |

---

## 🚀 **8. Deployment (Optional)**

| Platform                      | Use               |
| ----------------------------- | ----------------- |
| **Render / Railway / Heroku** | Host Django app   |
| **PostgreSQL**                | Cloud DB          |
| **Gunicorn + Nginx**          | Production server |

---

## ✅ **Summary**

**Plan Overview**

- **Language:** Python
- **Framework:** Django
- **Database:** SQLite → PostgreSQL
- **Frontend:** Bootstrap 5 + Django Templates
- **Reusable Components:** navbar, alerts, form, table, modal, pagination
- **Focus:** Simplicity, reusability, maintainability

---
