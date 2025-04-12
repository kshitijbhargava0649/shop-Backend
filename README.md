
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
