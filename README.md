# Inventory Fi - Backend

This is a backend server for the Inventory Fi application, using Node.js, Express, and direct PostgreSQL queries via the `pg` library.

## Setup Instructions

### Prerequisites

* [Node.js](https://nodejs.org/) (v14 or higher)
* [PostgreSQL](https://www.postgresql.org/download/) (Make sure the service is running)
* A PostgreSQL client like `psql` or a GUI like `pgAdmin`.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd inventory_fi
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project and add your database credentials and JWT secret.
    ```env
    # .env file
    PORT=8080
    
    # PostgreSQL Connection
    DB_USER=postgres
    DB_PASSWORD=your_db_password
    DB_NAME=inventory_fi_db
    DB_HOST=127.0.0.1
    DB_PORT=5432
    
    # JWT Secret
    JWT_SECRET=this_is_a_very_secret_key_change_it
    ```

4.  **Create the Database:**
    Using `psql` or a GUI tool, connect to your PostgreSQL instance and create the database you specified in the `.env` file (e.g., `inventory_fi_db`).
    ```sql
    CREATE DATABASE inventory_fi_db;
    ```

5.  **Initialize the Database Schema:**
    Run the initialization script to create the `users` and `products` tables in your database. This script executes the commands in `db/schema.sql`.
    ```bash
    npm run db:init
    ```

6.  **Start the server:**
    For development with auto-reloading:
    ```bash
    npm run dev
    ```
    For production:
    ```bash
    npm start
    ```
    The server will start on the port specified in your `.env` file (default is `8080`).

## API Documentation (Swagger/OpenAPI)

This documentation describes the REST APIs available. You can use this with tools like the [Swagger Editor](https://editor.swagger.io/) to visualize and interact with the API.

```yaml
openapi: 3.0.0
info:
  title: Inventory Fi API
  description: REST APIs for managing users and products for the Inventory Fi application.
  version: 1.0.0
servers:
  - url: http://localhost:8080/api
    description: Development server

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: The auto-generated ID of the user.
        username:
          type: string
          description: User's unique username.
        created_at:
          type: string
          format: date-time
          description: The date and time the user was created.
    Product:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: The auto-generated ID of the product.
        name:
          type: string
        type:
          type: string
        sku:
          type: string
          description: Unique stock keeping unit.
        image_url:
          type: string
          format: uri
        description:
          type: string
        quantity:
          type: integer
        price:
          type: number
          format: float
        created_at:
          type: string
          format: date-time
    LoginCredentials:
      type: object
      required:
        - username
        - password
      properties:
        username:
          type: string
        password:
          type: string
    NewProduct:
      type: object
      required:
        - name
        - type
        - sku
        - quantity
        - price
      properties:
        name:
          type: string
        type:
          type: string
        sku:
          type: string
        image_url:
          type: string
        description:
          type: string
        quantity:
          type: integer
        price:
          type: number
    UpdateQuantity:
        type: object
        required:
            - quantity
        properties:
            quantity:
                type: integer
                description: The new quantity for the product.
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

paths:
  /auth/register:
    post:
      summary: Register a new user
      tags: [Auth]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginCredentials'
      responses:
        '201':
          description: User registered successfully.
        '400':
          description: Bad request (e.g., user already exists, missing fields).

  /auth/login:
    post:
      summary: Login a user
      tags: [Auth]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginCredentials'
      responses:
        '200':
          description: Login successful, returns JWT token.
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
        '400':
          description: Invalid credentials.

  /products:
    post:
      summary: Add a new product
      tags: [Products]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewProduct'
      responses:
        '201':
          description: Product added successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  product_id:
                    type: string
                    format: uuid
        '401':
          description: Unauthorized (invalid or missing token).
    get:
      summary: Get a list of all products
      tags: [Products]
      security:
        - bearerAuth: []
      parameters:
        - name: page
          in: query
          description: Page number for pagination.
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          description: Number of items per page.
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: A paginated list of products.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Product'
        '401':
          description: Unauthorized.

  /products/{id}/quantity:
    put:
      summary: Update a product's quantity
      tags: [Products]
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          description: The ID of the product to update.
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateQuantity'
      responses:
        '200':
          description: Product quantity updated successfully.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
        '401':
          description: Unauthorized.
        '404':
          description: Product not found.
