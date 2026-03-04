# Setup Instructions

## 1. Clone the Repository

```
git clone https://github.com/Vivek971/assignment-east-vantage.git
cd <project-folder>
```

## 2. Create Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

Start the FastAPI server using:

```bash
python main.py
```

The API will start at:

```
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# Example API Usage

### Create Place

POST `/places`

```json
{
  "address": "Connaught Place",
  "latitude": 28.6315,
  "longitude": 77.2167
}
```

---

### Find Nearby Places

POST `/places/nearby`

```json
{
  "latitude": 28.6139,
  "longitude": 77.209,
  "radius_km": 5,
  "limit": 10
}
```

---

# Logging

Application logs are stored in:

```
logs/app.log
```

The logger records API requests, responses, and errors.

---

# Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
