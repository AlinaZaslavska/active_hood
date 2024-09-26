# Project Overview

**App Purpose:** Creating an app that connects people in Germany based on their city and interests in sports or art, facilitating interactions between trainers and participants.

## Key Features

1. **User Authentication and Authorization**

   - Sign up, log in, and log out
   - User profiles

2. **Event Management**

   - Create, view, edit, and delete events
   - Search events by city

3. **Event Participation**
   - Users can join or leave events

## Tech Stack

- **Backend:**

  - **Django (Python)** for web framework
  - **Django Rest Framework (DRF)** for API creation
  - **Django ORM** for database management

- **Database:**

  - **PostgreSQL** for data storage

- **Authentication:**
  - **JWT (JSON Web Tokens)** for secure user authentication

**ActiveHood Project Setup**

**System Requirements:**

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)

**Setting Up on Windows:**

1. Installing Python:

   - Download the latest Python installer from the official Python website.
   - Run the installer and ensure the option "Add Python to PATH" is checked.
   - Complete the installation.

2. Creating and Activating a Virtual Environment:

   - Open Command Prompt.
   - Navigate to the project directory.
   - Create a virtual environment by running the command: `python -m venv venv`.
   - Activate the virtual environment by running: `venv\Scripts\activate`.

3. Installing Dependencies:

   - With the virtual environment activated, install the required packages using the command: `pip install -r requirements.txt`.

4. Running Migrations:
   - Apply database migrations by running the following commands in sequence: `python manage.py makemigrations` and `python manage.py migrate`.

**Setting Up on macOS:**

1. Installing Python:

   - Open Terminal.
   - Use Homebrew to install Python by running the command: `brew install python`.
   - Alternatively, you can download the installer from the official Python website.

2. Creating and Activating a Virtual Environment:

   - Open Terminal and navigate to the project directory.
   - Create a virtual environment by running the command: `python3 -m venv venv`.
   - Activate the virtual environment by running: `source venv/bin/activate`.

3. Installing Dependencies:

   - With the virtual environment activated, install the required packages using the command: `pip install -r requirements.txt`.

4. Running Migrations:
   - Apply database migrations by running the following commands in sequence: `python manage.py makemigrations` and `python manage.py migrate`.

**Setting Up on Linux:**

1. Installing Python:

   - Open Terminal.
   - Install Python using the package manager:
     - For Ubuntu/Debian: `sudo apt update` and then `sudo apt install python3 python3-venv python3-pip`.
     - For CentOS/RHEL: `sudo yum install python3 python3-venv python3-pip`.

2. Creating and Activating a Virtual Environment:

   - Navigate to the project directory.
   - Create a virtual environment by running the command: `python3 -m venv venv`.
   - Activate the virtual environment by running: `source venv/bin/activate`.

3. Installing Dependencies:

   - With the virtual environment activated, install the required packages using the command: `pip install -r requirements.txt`.

4. Running Migrations:
   - Apply database migrations by running the following commands in sequence: `python manage.py makemigrations` and `python manage.py migrate`.

**Common Setup Steps:**

1. .env Configuration:

   - Create a `.env` file in the root directory (where `manage.py` is located) with the following variables. Replace the placeholder values with your actual credentials:
     - SECRET_KEY: Your secret key
     - DB_NAME: Your database name
     - DB_USER: Your database user
     - DB_PASS: Your database password
     - EMAIL_USER: Your email address
     - EMAIL_HOST_PASSWORD: Your email password

2. Database Setup:

   - Ensure you have PostgreSQL installed and running on your machine. Create a database for the project using the following steps:
     - Create a database named `activehood`.
     - Create a user with a password.
     - Grant all privileges on the `activehood` database to the user.
   - Update the `DATABASES` configuration in the `settings.py` file as needed.

3. Google OAuth Integration:

   - Visit the Google Cloud Console.
   - Create a new project.
   - Configure the OAuth consent screen and create OAuth 2.0 Client IDs:
     - Navigate to APIs & Services > OAuth consent screen.
     - Choose External and create the consent screen by filling in the required fields such as App name, User support email, and Developer contact information.
     - Save and continue.
     - Navigate to APIs & Services > Credentials.
     - Create credentials by selecting OAuth 2.0 Client ID.
     - Choose Web application.
     - Enter a name for the client and add the URI where your application will handle OAuth 2.0 responses, typically `http://127.0.0.1:8000/oauth/complete/google-oauth2/`.
     - Create and download the OAuth credentials.
   - Update your `settings.py` with your client ID, client secret, and redirect URI.

4. Email Configuration:
   - To configure your Gmail account for sending emails via Django, update the following settings in your `settings.py` file:
     - EMAIL_BACKEND: `'django.core.mail.backends.smtp.EmailBackend'`
     - EMAIL_HOST: `'smtp.gmail.com'`
     - EMAIL_USE_TLS: `True`
     - EMAIL_PORT: `587`
     - EMAIL_HOST_USER: Set this to your email address
     - EMAIL_HOST_PASSWORD: Set this to your email password
   - Optionally, enable Less Secure Apps in your Google account settings for testing purposes.
