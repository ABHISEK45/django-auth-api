# Django Authentication API

A Django REST Framework authentication system implementing OTP-based registration, cookie-based authentication, protected user endpoints, and Swagger API documentation.

## Features

* User Registration with Email OTP Verification
* OTP-based Account Activation
* Login using Email and Password
* HttpOnly Cookie-based Authentication
* Protected User Details Endpoint
* Logout Functionality
* Swagger API Documentation
* CSRF Token Generation Endpoint

## Tech Stack

* Python 3
* Django 6
* Django REST Framework
* DRF Authtoken
* drf-yasg (Swagger)

## Setup Instructions

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

Swagger UI:

```text
http://127.0.0.1:8000/swagger/
```

## API Endpoints

### Register

POST `/api/register/`

Registers a user and sends OTP to the provided email address.

### Verify Registration

POST `/api/register/verify/`

Verifies the OTP and activates the account.

### Login

POST `/api/login/`

Authenticates the user and sets an HttpOnly cookie named `auth_token`.

### Current User

GET `/api/me/`

Returns details of the authenticated user.

### Logout

POST `/api/logout/`

Deletes the authentication token and clears the cookie.

## Authentication Flow

1. Register using email and password.
2. Receive OTP.
3. Verify OTP.
4. Login using email and password.
5. Server creates an authentication token.
6. Token is stored in an HttpOnly cookie.
7. Protected endpoints use the cookie for authentication.
8. Logout revokes the token.

## Security Features

* HttpOnly Authentication Cookies
* Cookie-based Authentication
* OTP Verification
* Protected Endpoints
* CSRF Token Generation Endpoint

## Project Structure

authentication/

* models.py
* views.py
* serializers.py
* urls.py
* authentication.py
* utils.py

config/

* settings.py
* urls.py
