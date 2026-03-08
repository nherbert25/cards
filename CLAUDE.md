# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Flask-based web application featuring a multiplayer blackjack game with real-time communication via WebSockets. The backend is Python/Flask with SQLAlchemy ORM, and the frontend uses TypeScript compiled to JavaScript with Socket.IO for real-time updates.

## Technology Stack

- **Backend**: Flask 3.0 with Flask-SocketIO for WebSocket support
- **Frontend**: TypeScript (ES2020), HTML/CSS, Socket.IO client
- **Database**: SQLAlchemy with SQLite (development/production) or in-memory (testing)
- **Session Management**: Flask-Session with SQLAlchemy backend
- **Authentication**: Flask-Bcrypt, Flask-Login
- **Testing**: pytest with pytest-env and pytest-mock
- **Deployment**: Gunicorn with eventlet worker class (required for WebSocket support)

## Development Commands

### Environment Setup
```bash
# macOS (uses pyenv)
make venv_mac

# Windows
make venv_windows
```

### Running the Application
```bash
# Development mode (allows unsafe werkzeug)
python -m cards.app

# Production (REQUIRED for WebSocket support)
gunicorn --worker-class eventlet -w 1 cards.app:app
```

**Important**: Gunicorn can only support 1 worker when using WebSockets with eventlet. Do not increase worker count.

### TypeScript Development
```bash
# Compile TypeScript to JavaScript (REQUIRED after any .ts file changes)
make build
# or
make ts_compile
# or directly
tsc --project ./tsconfig.json
```

TypeScript source files are in `cards/static/js/**/*.ts` and compile to JavaScript in the same directory.

### Testing
```bash
# Run tests (excludes end-to-end tests)
make test
# or
pytest --ignore=tests/blackjack/test_blackjack_end_to_end.py

# Run all tests including end-to-end
make test_all
# or
pytest

# Run with coverage report
make coverage
```

### Linting
```bash
make flake8.check
```

### Git Branch Cleanup
```bash
# Preview branches to delete
make preview-cleanup

# Delete merged branches
make cleanup
```

## Architecture

### Application Factory Pattern
The app uses Flask's application factory pattern defined in `cards/app_setup.py`:
- `create_app()` creates and configures the Flask application
- Configuration is selected based on `FLASK_ENV` environment variable (development/testing/production)
- Extensions (db, session, bcrypt, socketio) are initialized with the app instance

### Entry Point
- `cards/app.py` - Creates the app instance and runs it with SocketIO
- Main application logic is in `cards/app_setup.py`

### Configuration
Three environment configurations in `cards/configs/config.py`:
- **DevelopmentConfig**: SQLite file database, CSRF disabled
- **TestingConfig**: In-memory SQLite database, CSRF disabled, `TESTING=True`
- **ProductionConfig**: SQLite file database, CSRF enabled

Set environment with: `export FLASK_ENV=testing|development|production`

### Blueprints
- `blackjack_blueprint` - Blackjack game routes and SocketIO handlers
- `landing_page_blueprint` - Landing page, login, registration routes

Blueprints are registered in `create_app()` to avoid circular imports.

### Blackjack Game Architecture
- **Models** (`cards/blackjack/*_model.py`): Card, Deck, Hand, Player, Blackjack game logic
- **Controller** (`cards/blackjack/controller.py`): Manages game state, provides `serialize_blackjack_data()` for frontend
- **Routes** (`cards/blackjack/routes.py`): Flask HTTP routes and SocketIO event handlers
- **Global Controller Instance**: A single `blackjack_controller` instance manages game state across WebSocket connections

### WebSocket Communication
Uses Flask-SocketIO on backend and Socket.IO client on frontend:

**Backend Events** (in `cards/blackjack/routes.py`):
- `@socketio.on('hit')` - Player hits
- `@socketio.on('stay')` - Player stays
- `@socketio.on('double_down')` - Player doubles down
- `@socketio.on('split_pair')` - Player splits pair
- `@socketio.on('new_game')` - Start new game
- `@socketio.on('rebuild_entire_page')` - Rebuild entire page
- `@socketio.on('request_game_data')` - Request current game state
- `@socketio.on('update_page_data')` - Update page data

**Backend Emissions**:
- `socketio.emit('update_page_data', data)` - Update specific game state
- `socketio.emit('rebuild_entire_page', data)` - Full page rebuild
- `socketio.emit('player_added_hand', data)` - Notify when player splits

**Frontend** (TypeScript in `cards/static/js/`):
- `blackjack.ts` - Main entry point, socket connection
- `components/eventListeners.ts` - Button click handlers
- `components/gameUI.ts` - DOM manipulation for game state
- `components/schemas.ts` - TypeScript interfaces for game data
- `components/buttons.ts` - Button UI management
- `components/debugger.ts` - Debug utilities

### Database
- **Models**: `cards/database/models.py` (User, Blackjack tables)
- **DAOs**: `cards/database/user_table_DAO.py`, `cards/database/blackjack_table_DAO.py`
- **Database Instance**: `db` initialized in `cards/database/database.py`, imported as singleton

### Testing Structure
- `tests/app/` - Landing page route tests
- `tests/blackjack/` - Blackjack game logic and route tests
- `tests/database/` - Database DAO tests
- `tests/pytest.ini` - Sets `FLASK_ENV=testing` for all tests
- `tests/blackjack/conftest.py` - Shared pytest fixtures for blackjack tests

## Important Notes

### TypeScript Compilation
Always run `make build` after modifying any `.ts` files. The compiled JavaScript is what the browser executes, not the TypeScript source.

### WebSocket Constraints
- Must use eventlet worker class with Gunicorn
- Can only run 1 worker process (WebSocket limitation)
- Development mode uses `allow_unsafe_werkzeug=True` in `socketio.run()`

### Global State
The `blackjack_controller` in `routes.py` is a global singleton that maintains game state. This works with the 1-worker constraint but would need refactoring for horizontal scaling.

### Running Single Tests
```bash
# Run specific test file
pytest tests/blackjack/test_blackjack_model.py

# Run specific test function
pytest tests/blackjack/test_blackjack_model.py::test_function_name

# Run with verbose output
pytest -v tests/blackjack/
```

### Database Migrations
Database tables are auto-created via `db.create_all()` in `initialize_db()`. This project does not use Alembic for migrations.

### Static Files
- CSS: `cards/static/css/`
- Images: `cards/static/images/`
- JavaScript (compiled from TypeScript): `cards/static/js/`
- Templates: `cards/templates/`

### Dependencies
Python dependencies are in `requirements.txt`. The project uses a custom package repository (nexus-repo.selflender.com) as seen in `pylock.toml`, but standard PyPI installation via `pip install -r requirements.txt` should work for development.
