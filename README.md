# Shop-Backend

A full-stack e-commerce application with Shopify integration, built using Flask and React.

## Tech Stack

### Backend
- Flask (Python)
- MongoDB (User Data)
- PostgreSQL (Event Logging)
- JWT Authentication
- Shopify GraphQL API Integration

### Frontend
- React
- Chakra UI
- Purity UI Dashboard
- Chart.js/Recharts

## Project Structure
```
shop-Backend/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   └── src/
├── docker/
│   ├── postgres/
│   └── mongodb/
└── docker-compose.yml
```

## Setup Instructions

1. Clone the repository
2. Set up environment variables
3. Install dependencies
4. Run the application

## Features

- User Authentication (JWT)
- Product Management with Shopify Integration
- Event Logging and Visualization
- Responsive UI with Chakra UI
- Data Table with Sorting and Filtering
- Real-time Product Updates

## API Endpoints

- POST /api/products: Create a new product
- GET /api/products: List all products
- GET /api/products/{id}: Retrieve product details
- PUT /api/products/{id}: Update a product
- DELETE /api/products/{id}: Delete a product

## Development

### Prerequisites
- Python 3.8+
- Node.js 14+
- Docker
- MongoDB
- PostgreSQL

### Installation

1. Backend Setup:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Frontend Setup:
```bash
cd frontend
npm install
```

3. Database Setup:
```bash
docker-compose up -d
```

### Running the Application

1. Start the backend:
```bash
cd backend
python run.py
```

2. Start the frontend:
```bash
cd frontend
npm start
```

## License

MIT