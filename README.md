# Flask ToDo App

A simple, robust, and clean ToDo list application built with **Python** and **Flask**. This application allows users to create, manage, and track their daily tasks with a minimal interface.

## 🚀 Features

* **Create Tasks**: Add new tasks to your list quickly.
* **Read Tasks**: View all incomplete and completed tasks.
* **Update Tasks**: Mark tasks as "Completed" or update their content.
* **Delete Tasks**: Remove tasks you no longer need.
* **Data Persistence**: Uses Postgresql (via SQLAlchemy) to save tasks so they aren't lost on refresh.

## 🛠️ Tech Stack

* **Backend**: Python 3, Flask
* **Database**: PostgreSQL, SQLAlchemy
* **Frontend**: HTML5, CSS3 (Jinja2 Templates)

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your machine:
* [Python 3.6+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Adrian7373/flask-ToDo.git](https://github.com/Adrian7373/flask-ToDo.git)
    cd flask-ToDo
    ```

2.  **Create a Virtual Environment** (Recommended)
    * *Windows*:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    * *macOS/Linux*:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  **Initialize the Database**
    If your application requires an initial database setup, run:
    ```bash
    python
    >>> from app import db, app
    >>> with app.app_context():
    ...     db.create_all()
    >>> exit()
    ```
    *(Note: If your app handles this automatically on startup, you can skip this step.)*

## 🏃‍♂️ Running the App

Start the development server:

```bash
flask run

```

*Or, if you have a main entry point script:*

```bash
python app.py

```

Open your browser and navigate to:
`http://127.0.0.1:5000/`

## 📂 Project Structure

```text
flask-ToDo/
├── static/              # CSS, Images, and JavaScript files
│   └── style.css
├── templates/           # HTML Templates (Jinja2)
│   ├── index.html
│   └── update.html
├── app.py               # Main application logic and routes
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

```

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Adrian7373**

* GitHub: [Adrian7373](https://www.google.com/search?q=https://github.com/Adrian7373)
