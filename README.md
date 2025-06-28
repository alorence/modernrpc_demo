# Django Modern RPC Demo

This is a demo website for [django-modern-rpc](https://github.com/alorence/django-modern-rpc), a Django library that helps you enable a JSON and XML-RPC server in your application.

## Features

- Django 4.2+ with Python 3.12+
- Tailwind CSS for styling
- JSON-RPC and XML-RPC support
- Docker support for production deployment

## Development Setup

### Prerequisites

- Python 3.12+
- Node.js and npm
- Poetry (for dependency management)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   poetry install
   ```
3. Install Tailwind CSS dependencies:
   ```
   cd theme/static_src
   npm install
   ```
4. Run Tailwind CSS in development mode:
   ```
   npm run dev
   ```
5. In a separate terminal, run the Django development server:
   ```
   poetry run python manage.py runserver
   ```

## Tailwind CSS

This project uses [Tailwind CSS](https://tailwindcss.com/) for styling. The Tailwind configuration is located in the `theme` app.

### Development

During development, Tailwind CSS is compiled on-the-fly. To start the Tailwind CSS compiler in watch mode:

```
cd theme/static_src
npm run dev
```

### Production

For production, Tailwind CSS is compiled and minified during the Docker build process. The compiled CSS is stored in `theme/static/css/dist/styles.css`.

## Docker Deployment

To build and run the Docker container:

```
docker build -t modernrpc-demo .
docker run -p 8000:8000 modernrpc-demo
```

The Docker container:
1. Installs all dependencies
2. Builds Tailwind CSS
3. Collects static files
4. Runs migrations
5. Starts the application with Gunicorn
