# Integration Project

A Django web application project for integration purposes.

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Quick Start](#quick-start)
- [Available Commands](#available-commands)
- [Project Structure](#project-structure)
- [Development](#development)
- [Database](#database)
- [Static Files](#static-files)
- [Contributing](#contributing)

## 🔧 Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment support

## 📦 Installation

### 1. Clone the repository (if applicable)

```bash
git clone <repository-url>
cd integration
```

### 2. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or use the makefile command:
```bash
make install
```

## 🚀 Project Setup

### 1. Run migrations

```bash
python manage.py migrate
```

Or use the makefile:
```bash
make migrate
```

### 2. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

Or use the makefile:
```bash
make superuser
```

## ⚡ Quick Start

1. Activate the virtual environment
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
   Or:
   ```bash
   make run
   ```

3. Open your browser and navigate to: `http://127.0.0.1:8000/`

## 📝 Available Commands

This project includes a `makefile` with convenient shortcuts for common Django tasks:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install packages from requirements.txt |
| `make run` | Start development server |
| `make migrate` | Apply database migrations |
| `make makemigrations` | Create new migrations |
| `make migrateall` | Create and apply migrations |
| `make shell` | Start Django shell |
| `make test` | Run tests |
| `make superuser` | Create superuser |
| `make collectstatic` | Collect static files |
| `make clean` | Clean cache files |
| `make format` | Format code (if black/autopep8 available) |

**Note:** On Windows, you may need to install `make` or use WSL (Windows Subsystem for Linux). Alternatively, you can run the commands directly using Python.

## 📁 Project Structure

```
integration/
├── integration_project/      # Main project package
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── venv/                    # Virtual environment (not tracked in git)
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── makefile                 # Quick command shortcuts
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 💻 Development

### Running the Development Server

```bash
python manage.py runserver
```

To run on a specific port:
```bash
python manage.py runserver 8080
```

### Creating Django Apps

```bash
python manage.py startapp app_name
```

### Django Shell

Access the Django shell for interactive debugging:
```bash
python manage.py shell
```

Or use:
```bash
make shell
```

### Running Tests

```bash
python manage.py test
```

Or:
```bash
make test
```

## 🗄️ Database

This project uses SQLite by default. The database file (`db.sqlite3`) will be created automatically after running migrations.

### Create Migrations

After modifying models:
```bash
python manage.py makemigrations
```

### Apply Migrations

```bash
python manage.py migrate
```

### Combined Command

Create and apply migrations in one step:
```bash
make migrateall
```

## 📂 Static Files

Django's static files (CSS, JavaScript, images) are configured to be served from the `static/` directory.

### Collect Static Files (for production)

```bash
python manage.py collectstatic
```

Or:
```bash
make collectstatic
```

## 🔒 Security Notes

⚠️ **Important:** Before deploying to production:

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False` in `settings.py`
3. Configure `ALLOWED_HOSTS` in `settings.py`
4. Use environment variables for sensitive data
5. Use a production-ready database (PostgreSQL, MySQL, etc.)
6. Set up proper static file serving
7. Enable HTTPS

## 🧹 Cleaning Up

To remove Python cache files:

```bash
make clean
```

This will remove:
- `__pycache__` directories
- `.pyc` files
- `.pyo` files

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available for use.

## 👤 Author

Your Name

---

**Happy Coding! 🚀**

