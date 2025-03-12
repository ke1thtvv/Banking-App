# Banking App

## Overview
The **Banking App** is a full-stack financial application that enables users to create accounts, manage balances, and perform secure fund transfers. Designed with a focus on security, transactional integrity, and scalability, this application follows modern software engineering best practices.

## Features
- **User Authentication & Authorization**: Secure login and account management using Flask-Login.
- **Multi-Account Management**: Users can create and manage multiple bank accounts under a single profile.
- **Secure Transactions**:
  - Atomic money transfers with database transactions ensuring consistency.
  - Real-time balance updates for intra-bank transfers.
  - Scheduled processing for inter-bank transfers.
- **Transaction History**: Users can review past transactions with filtering options.
- **Responsive UI**: Flask-based frontend with Bootstrap for enhanced UX.

## Tech Stack
### Backend:
- **Flask** – Lightweight and modular web framework.
- **SQLAlchemy** – ORM for database interactions.
- **SQLite/PostgreSQL** – Data persistence with ACID-compliant transactions.
- **Flask-Login** – Secure user authentication and session management.

### Frontend:
- **Jinja2 Templates** – Server-side rendering for dynamic UI.
- **Bootstrap** – Modern styling and responsiveness.

### Deployment:
- **Gunicorn** – Production-ready WSGI server.
- **Docker (Optional)** – Containerized deployment.

## Database Schema
### Tables:
1. **User** (`id`, `username`, `password_hash`, `email`)
2. **Account** (`id`, `user_id`, `name`, `balance`, `bank_id`)
3. **Transfer** (`id`, `from_account_id`, `to_account_id`, `amount`, `status`, `timestamp`)

## Transaction Workflow
1. User initiates a transfer request.
2. System verifies balance sufficiency and recipient validity.
3. Transaction is executed atomically:
   - **Same-bank transfer**: Instantly updates balances.
   - **Inter-bank transfer**: Schedules transaction with a `pending` status.
4. Database commits only if all steps succeed, preventing data loss.

## Setup & Installation
### Prerequisites:
- Python 3.9+
- Flask & Dependencies (`pip install -r requirements.txt`)
- SQLite/PostgreSQL (configured in `.env`)

### Running Locally:
```bash
# Clone the repository
git clone https://github.com/yourusername/banking-app.git
cd banking-app

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
flask run
```

### Running with Docker:
```bash
docker build -t banking-app .
docker run -p 5000:5000 banking-app
```

## API Endpoints
| Method | Endpoint         | Description                  |
|--------|----------------|------------------------------|
| `POST` | `/register`    | Register a new user          |
| `POST` | `/login`       | Authenticate a user          |
| `GET`  | `/accounts`    | Get user’s accounts          |
| `POST` | `/transfer`    | Execute a money transfer     |
| `GET`  | `/history`     | Retrieve transaction history |

## Security Measures
- **Hashed Passwords**: Using PBKDF2 for secure authentication.
- **Database Transactions**: Atomic commits to prevent partial transfers.
- **Role-Based Access Control**: Prevents unauthorized actions.
- **Input Validation**: Prevents SQL Injection and XSS attacks.

## Future Enhancements
- Implementing **two-factor authentication (2FA)**.
- Adding **external bank APIs** for real-world transactions.
- Enhancing **audit logs** for transaction tracking.

## Contact & Contributions
For any queries or contributions, please create an issue or submit a pull request.

---
**GitHub:** [ke1thtvv](https://github.com/ke1thtvv)
