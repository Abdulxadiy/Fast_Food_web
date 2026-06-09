# MaxWay — Fast Food Web Platform

<p align="center">
  A Django-based fast-food ordering website with a customer storefront, shopping cart, checkout flow, and a custom admin dashboard for catalog and order management.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/Interface-Uzbek-success?style=for-the-badge" alt="Uzbek UI">
</p>

## Overview

**MaxWay** is a full-stack web application for a fast-food business. Customers can browse the menu, add items to a cart, fill in delivery details, and place orders from the browser. Returning customers can be recognized by phone number and have their profile auto-filled.

The project also includes a **custom admin panel** for authenticated staff to manage categories, products, customers, and orders, plus a dashboard with sales overview and top-selling products.

## What This Project Can Do

### Customer features

- Browse products grouped by category on the storefront homepage.
- View product details including name, price, description, and image.
- Add products to a browser-based cart with quantity tracking.
- Persist cart state in `localStorage` between page visits.
- Open a floating cart panel with total price and checkout action.
- Complete checkout with first name, last name, phone, email, and delivery address.
- Auto-fill customer data when a known phone number is entered.
- Choose a payment method: **cash** or **card** (UzCard / Humo).
- Submit orders via AJAX and receive a success confirmation.
- Store customer and order data in PostgreSQL.

### Admin / staff features

- Secure login and logout using Django authentication.
- Dashboard overview with counts for categories, products, customers, and orders.
- View category-to-product distribution on the dashboard.
- See top 10 best-selling products based on order history.
- Full CRUD for categories.
- Full CRUD for products, including image upload.
- Full CRUD for customer records.
- View all incoming orders with status, payment type, address, and date.
- Inspect ordered items for each order.
- View order history for a specific customer.
- Track recent admin actions in the session (create/edit/delete logs).
- Access a profile page from the admin sidebar.

## Tech Stack

| Area | Technology |
|---|---|
| Main language | Python 3.11 |
| Web framework | Django 5.2 |
| Database | PostgreSQL 16 |
| App server | Gunicorn |
| Static files | WhiteNoise |
| Image handling | Pillow |
| DB driver | psycopg2 |
| Containerization | Docker + Docker Compose |
| Frontend | Django templates, custom CSS, vanilla JavaScript |

## Supported Languages

This project uses a **Uzbek-facing customer interface** for menu browsing and checkout.

Programming language used in the codebase:

- Python

Admin panel labels and dashboard text are primarily in English.

## Project Structure

```text
MaxWay/
├── manage.py                          # Django management entry point
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Web service image
├── docker-compose.yml                 # PostgreSQL + Django services
├── entrypoint.sh                      # Migrate, collectstatic, run Gunicorn
├── maxway/                            # Project settings and root URLs
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── maxway_users/                      # Customer-facing app
│   ├── models.py                      # Category, Product, Users, Order, OrderProduct
│   ├── views.py                       # Storefront and checkout views
│   ├── urls.py
│   └── services.py                    # Raw SQL helpers
├── maxway_admin/                      # Custom admin panel
│   ├── views.py                       # Dashboard and CRUD views
│   ├── urls.py
│   ├── forms.py                       # Model forms for admin CRUD
│   ├── services.py                    # Reporting and detail queries
│   └── management/commands/
│       └── init_superuser.py          # Auto-create default superuser
├── templates/
│   ├── maxway_users/                  # Storefront and order pages
│   └── maxway_admin/                  # Admin dashboard and CRUD pages
├── static/
│   ├── maxway_users/                  # Storefront CSS, JS, images
│   └── maxway_admin/                  # Admin theme assets
├── media/                             # Uploaded product images
└── staticfiles/                       # Collected static files
```

## Order Flow

1. Customer opens the homepage and browses categories and products.
2. Customer adds items to the cart; cart data is saved in `localStorage`.
3. Customer opens the order page from the cart.
4. Customer enters contact details and delivery address.
5. If the phone number already exists, previous profile data is loaded automatically.
6. Customer selects a payment method: cash or card.
7. Order and order items are saved to PostgreSQL inside a database transaction.
8. Customer receives a success response with the new order ID.
9. Admin reviews the order from the admin panel.

## Database Design

The main application models live in `maxway_users` and include:

- `Category`
- `Product`
- `Users`
- `Order`
- `OrderProduct`

These tables cover:

- product catalog and categories
- customer contact and delivery information
- placed orders and payment type
- individual items inside each order

Django's built-in `auth_user` table is used for admin authentication.

## Configuration

The project reads configuration from environment variables.

### Required environment variables

```env
DJANGO_SECRET_KEY=your-secret-key

DB_NAME=maxway_db
DB_USER=maxway_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### Optional superuser bootstrap variables

Used by `init_superuser` during Docker startup:

```env
DJANGO_SUPERUSER_USERNAME=abdulxadiy
DJANGO_SUPERUSER_EMAIL=admin@maxway.local
DJANGO_SUPERUSER_PASSWORD=0000
```

### Config fields

- `DJANGO_SECRET_KEY`: Django secret key for sessions and security.
- `DB_NAME`: PostgreSQL database name.
- `DB_USER`: PostgreSQL username.
- `DB_PASSWORD`: PostgreSQL password.
- `DB_HOST`: Database host (`db` in Docker, `localhost` locally).
- `DB_PORT`: Database port, usually `5432`.
- `DJANGO_SUPERUSER_*`: Default admin account created on first container start.

Important:

- Do not commit real secrets to GitHub.
- `.env` is ignored by git; create it locally or use Docker Compose environment values.
- `DEBUG` is currently enabled in `settings.py`; disable it before production deployment.

## Installation

### Option 1: Docker Compose (recommended)

```bash
git clone https://github.com/Abdulxadiy/Fast_Food_web.git
cd MaxWay
docker compose up --build
```

The app will be available at:

```text
http://localhost:8000/
```

Admin panel:

```text
http://localhost:8000/maxway_admin/login_page/
```

### Option 2: Local development

```bash
git clone https://github.com/Abdulxadiy/Fast_Food_web.git
cd MaxWay
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Create a PostgreSQL database, export the environment variables from the configuration section, then run:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py init_superuser
python manage.py runserver
```

## Run

### Docker

```bash
docker compose up
```

### Local

```bash
python manage.py runserver
```

Customer storefront:

```text
/
```

Checkout page:

```text
/order/
```

Admin dashboard:

```text
/maxway_admin/
```

Django built-in admin:

```text
/admin/
```

## Main Functional Modules

| File | Responsibility |
|---|---|
| `maxway_users/views.py` | Storefront, product AJAX lookup, checkout and order creation |
| `maxway_users/models.py` | Core business models for catalog, users, and orders |
| `maxway_users/services.py` | Product and user lookup helpers |
| `maxway_admin/views.py` | Admin login, dashboard, and CRUD pages |
| `maxway_admin/forms.py` | Admin forms for categories, products, and users |
| `maxway_admin/services.py` | Order detail queries and sales statistics |
| `templates/maxway_users/index.html` | Menu page, cart UI, and `localStorage` cart logic |
| `templates/maxway_users/order.html` | Checkout form, payment choice, order submission |
| `templates/maxway_admin/index.html` | Admin overview dashboard |
| `entrypoint.sh` | Waits for PostgreSQL, migrates DB, starts Gunicorn |
| `init_superuser.py` | Creates default admin user if missing |

## Docker Services

`docker-compose.yml` defines two services:

| Service | Purpose |
|---|---|
| `db` | PostgreSQL 16 with persistent volume |
| `web` | Django app built from `Dockerfile`, exposed on port `8000` |

On startup, the web container automatically:

1. Waits for PostgreSQL to become healthy
2. Runs migrations
3. Collects static files
4. Creates the default superuser if needed
5. Starts Gunicorn with 2 workers

## Payment Types

| Value | Meaning |
|---|---|
| `1` | Cash (`Naqd pul`) |
| `2` | Card (`UzCard` / `Humo`) |

## Why This Project Is Useful

MaxWay is a practical example of how a local fast-food business can run ordering operations through a modern web interface instead of only phone calls or third-party apps. It combines:

- a polished customer storefront
- cart and checkout handling
- customer recognition by phone number
- product image management
- admin-side catalog control
- order inspection and sales reporting

in one Django project with Docker support.

## Notes

- Cart data is stored in the browser via `localStorage`, not on the server.
- Product images are uploaded to `media/product_images/`.
- Order `status` is stored as an integer and currently defaults to `0`.
- Some admin reporting queries use raw SQL for joins and grouped statistics.
- Static assets are served through WhiteNoise in production mode.
- The custom admin panel is separate from Django's default `/admin/` interface.

## Future Improvements

- Move all secrets and database settings to a dedicated `.env.example` file.
- Add order status management from the admin panel.
- Replace integer payment/status codes with explicit model choices.
- Add automated tests for checkout and admin CRUD flows.
- Add REST API support for a mobile app.
- Add email or SMS notifications for new orders.
- Add role-based permissions for multiple staff accounts.
- Improve production settings: `DEBUG = False`, stricter `ALLOWED_HOSTS`, HTTPS support.
- Add CI/CD pipeline for build and deployment.

## License

This project is licensed under the [MIT License](LICENSE).
