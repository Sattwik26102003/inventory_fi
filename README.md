# Inventory Fi - Backend

This is a backend server for the **Inventory Fi** application, using **Node.js**, **Express**, and direct **PostgreSQL** queries via the `pg` library. The entire application stack, including the database, can be run using **Docker Compose**.

---

## 🚀 Setup & Running with Docker Compose (Recommended)

This is the simplest and recommended way to get the entire application, including the database, up and running with a single command.

### ✅ Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

### 📄 Step 1: Create the `.env` File

Create a file named `.env` in the root of the project. This file will provide the configuration for both the Node.js app and the PostgreSQL database container.

> ℹ️ **Important:** The `DB_HOST` must be the service name defined in `docker-compose.yml`, which is `db`.

```env
# .env file
PORT=8080

# PostgreSQL Connection
DB_USER=postgres
DB_PASSWORD=your_super_secret_password
DB_NAME=inventory_fi_db
DB_HOST=db  # <-- Must match the service name in docker-compose
DB_PORT=5432

# JWT Secret
JWT_SECRET=this_is_a_very_secret_key_change_it
