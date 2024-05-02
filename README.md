# PoseFitAI Backend API

## Overview
PoseFitAI is a backend service designed to manage fitness session data, including exercises like squats and planks. It allows users to register, login, start workout sessions, record exercise metrics, and view session histories.

## Getting Started

### Prerequisites
- Python 3.8+
- Flask
- SQLAlchemy
- Flask-JWT-Extended

### Installation

Clone the repository:
```bash
git clone https://yourrepository.com/PoseFitAI.git
cd PoseFitAI
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
Start the server:
```bash
flask run
```

The server will start on `http://127.0.0.1:5000`.

## API Endpoints

### User Authentication

- **POST /auth/register**
  - Description: Register a new user.
  - Body:
    ```json
    {
      "username": "alex",
      "email": "alex@example.com",
      "password": "alexpassword",
      "gender": "male",
      "height": 170,
      "weight": 80
    }
    ```

- **POST /auth/login**
  - Description: Authenticate a user and return a JWT.
  - Body:
    ```json
    {
      "username": "smith",
      "password": "smithpassword"
    }
    ```

### Session Management

- **GET /session/start**
  - Description: Start a new session.
  - Authorization: Bearer Token

- **POST /session/update**
  - Description: Update an ongoing session.
  - Body:
    ```json
    {
      "correct": 10,
      "incorrect": 5
    }
    ```
  - Authorization: Bearer Token

- **POST /session/end**
  - Description: End a session and record final details.
  - Body:
    ```json
    {
      "correct": 10,
      "incorrect": 5
    }
    ```
  - Authorization: Bearer Token

### Exercise Tracking

- **POST /plank/add**
  - Description: Add or update plank exercise data.
  - Body:
    ```json
    {
      "correct": 3,
      "incorrect": 1,
      "feedback": {
        "0": 5,
        "1": 3,
        "2": 7,
        "3": 2
      }
    }
    ```
  - Authorization: Bearer Token

- **GET /plank/get**
  - Description: Retrieve plank exercise data.
  - Authorization: Bearer Token

- **POST /squat/add**
  - Description: Add or update squat exercise data.
  - Body:
    ```json
    {
      "correct": 3,
      "incorrect": 1,
      "feedback": {
        "0": 5,
        "1": 3,
        "2": 7,
        "3": 2
      }
    }
    ```
  - Authorization: Bearer Token

- **GET /squat/get**
  - Description: Retrieve squat exercise data.
  - Authorization: Bearer Token

## Authentication
This API uses JWT for authentication. Ensure to include the `Authorization` header with your requests where required. Example:
```plaintext
Authorization: Bearer <Your-Token-Here>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
