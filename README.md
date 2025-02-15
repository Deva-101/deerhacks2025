# Project Setup Instructions for `brain`

## Overview
This document provides step-by-step instructions for setting up the Django project `brain` with the main app `brainrot`. The core functionality resides in the `views.py` file.

---

## **1. Clone the Repository**

```bash
git clone https://github.com/Deva-101/deerhacks2025.git
cd deerhacks2025
```

---

## **2. Set Up a Virtual Environment**

Create and activate a virtual environment to isolate dependencies:

```bash
# For Linux/MacOS:
python3 -m venv venv
source venv/bin/activate

# For Windows:
python -m venv venv
venv\Scripts\activate
```

---

## **3. Install Required Dependencies**

Install the required Python packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## **4. Set Up the Project**

Run the following command to apply database migrations and set up the schema:

```bash
python manage.py migrate
```

---

## **5. Run the Development Server**

Start the Django development server to verify the project setup:

```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000` to ensure the application is running.

---
