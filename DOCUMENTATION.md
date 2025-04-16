# Dookan App Documentation

## Overview
Dookan is a backend application built with Flask that provides API endpoints for a Shopify-like e-commerce platform. The application uses both PostgreSQL and MongoDB databases to store different types of data.

## Architecture

### Tech Stack
- **Backend Framework**: Flask 3.0.2
- **API Documentation**: Flask-RESTX
- **Databases**: 
  - PostgreSQL 14 (Relational Database)
  - MongoDB (Document Database)
- **Authentication**: JWT (JSON Web Tokens)
- **Containerization**: Docker

### Application Structure
The application follows a modular structure with the following main components:

1. **Authentication Module** (`app/auth/`)
   - Handles user authentication and authorization
   - JWT token management

2. **Products Module** (`app/products/`)
   - Manages product-related operations
   - Product CRUD operations

3. **Events Module** (`app/events/`)
   - Handles event-related operations
   - Event tracking and management

4. **Utils** (`app/utils/`)
   - Common utilities and helper functions

## Database Design

### MongoDB Collections

#### Users Collection (`identifier_users`)
```json
{
    "_id": ObjectId,
    "name": String (required, max_length: 100),
    "email": String (required, unique),
    "hashed_password": String (required),
    "is_active": Boolean (default: true)
}
```
Indexes:
- email (unique)

#### Products Collection (`identifier_products`)
```json
{
    "_id": ObjectId,
    "shopify_id": String (required, unique),
    "title": String (required),
    "description": String,
    "price": Float (required),
    "sku": String,
    "image_url": String
}
```
Indexes:
- shopify_id (unique)

### PostgreSQL Tables

#### Events Table (`identifier_events`)
```sql
CREATE TABLE identifier_events (
    event_id SERIAL PRIMARY KEY,
    event_type VARCHAR(20) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    product_id VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
Indexes:
- Composite index on (user_id, timestamp)
- Composite index on (event_type, timestamp)

## API Documentation

### Authentication API (`/api/auth`)

#### Sign Up
- **Endpoint**: `POST /api/auth/signup`
- **Request Body**:
```json
{
    "name": "string",
    "email": "string",
    "password": "string"
}
```
- **Response**:
```json
{
    "token": "string",
    "user": {
        "id": "string",
        "name": "string",
        "email": "string"
    }
}
```

#### Login
- **Endpoint**: `POST /api/auth/login`
- **Request Body**:
```json
{
    "email": "string",
    "password": "string"
}
```
- **Response**: Same as Sign Up

### Products API (`/api/products`)

#### Get All Products
- **Endpoint**: `GET /api/products`
- **Response**:
```json
[
    {
        "id": "string",
        "shopify_id": "string",
        "title": "string",
        "description": "string",
        "price": number,
        "sku": "string",
        "image_url": "string"
    }
]
```

#### Get Product by ID
- **Endpoint**: `GET /api/products/{id}`
- **Response**: Single product object

#### Create Product
- **Endpoint**: `POST /api/products`
- **Request Body**:
```json
{
    "shopify_id": "string",
    "title": "string",
    "description": "string",
    "price": number,
    "sku": "string",
    "image_url": "string"
}
```

#### Update Product
- **Endpoint**: `PUT /api/products/{id}`
- **Request Body**: Same as Create Product

#### Delete Product
- **Endpoint**: `DELETE /api/products/{id}`

### Events API (`/api/events`)

#### Get Events
- **Endpoint**: `GET /api/events`
- **Query Parameters**:
  - `user_id`: Filter by user
  - `event_type`: Filter by event type
  - `start_date`: Filter by start date
  - `end_date`: Filter by end date
- **Response**:
```json
[
    {
        "event_id": number,
        "event_type": "string",
        "user_id": "string",
        "product_id": "string",
        "timestamp": "string (ISO format)"
    }
]
```

#### Create Event
- **Endpoint**: `POST /api/events`
- **Request Body**:
```json
{
    "event_type": "string",
    "user_id": "string",
    "product_id": "string"
}
```

## Development Setup

### Prerequisites
- Python 3.x
- Docker and Docker Compose
- PostgreSQL 14
- MongoDB

### Environment Setup
1. Create a `.env` file with necessary environment variables
2. Install dependencies: `pip install -r requirements.txt`
3. Start the databases: `docker-compose up -d`
4. Run the application: `python main.py`

## Security
- JWT-based authentication
- Password hashing using bcrypt
- Environment-based configuration
- CORS support for API endpoints

## Testing
The application includes a test suite located in the `tests/` directory.

## Logging
Application logs are stored in `app.log`

## Deployment
The application is containerized using Docker and can be deployed using the provided `docker-compose.yml` file. 