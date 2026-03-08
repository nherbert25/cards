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

## Test Development Workflow

### MANDATORY: Test-Driven Development Feedback Loop

When writing or modifying tests, **ALWAYS** follow this workflow to ensure tests work correctly:

1. **Write the test** - Create or modify test file
2. **Run the test immediately** - Execute the specific test file or function:
   ```bash
   source venv/bin/activate && pytest tests/path/to/test_file.py -v
   ```
3. **Fix any failures** - If tests fail, fix them immediately before moving on
4. **Run full test suite** - After fixing individual tests, run the full suite:
   ```bash
   source venv/bin/activate && pytest tests/ -v
   ```
5. **Iterate** - Repeat steps 2-4 until all tests pass

### Common Testing Pitfalls and Solutions

#### Flask Application Context Required
**Problem**: `RuntimeError: Working outside of application context`

**Solution**: Tests that use database operations, render templates, or Flask features need app context:

```python
@pytest.fixture
def app_context():
    from cards.app import app
    with app.app_context():
        yield

def test_something(app_context):
    # Test code that needs Flask app context
```

#### Mocking Database Operations
**Problem**: Tests calling real database instead of mocks

**Solution**: Always mock database calls in unit tests:

```python
@pytest.fixture
def controller(self, mocker):
    # Mock database operations to avoid DB dependencies
    mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
    mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)
    return BlackjackController()
```

#### SocketIO Testing
**Problem**: SocketIO events not being captured in tests

**Solution**: Use `socketio_client` fixture and check received messages:

```python
def test_socketio_event(self, client, socketio_client):
    socketio_client.emit('hit', {'user_id': 'test-uuid', 'hand_index': 0})
    received = socketio_client.get_received()
    assert len(received) > 0
```

#### Invalid User/Player Handling
**Problem**: Code assumes player exists, crashes on None

**Solution**: Test should expect None or early return:

```python
def test_invalid_player(self, controller):
    # Should handle gracefully, not crash
    controller.hit('invalid-uuid', 0)  # Should log error, not raise exception
```

#### Deck Shuffling in Tests
**Problem**: Tests produce non-deterministic results due to shuffle

**Solution**: Mock shuffle to control card order:

```python
def test_game_flow(self, mocker):
    mocker.patch.object(game.deck, 'shuffle')  # Prevents random shuffle
```

### Test Categories

1. **Unit Tests** - Test individual functions/methods in isolation with mocking
2. **Integration Tests** - Test multiple components working together, may use real DB
3. **Route Tests** - Test Flask routes and SocketIO handlers
4. **End-to-End Tests** - Full application flow tests (in `test_blackjack_end_to_end.py`)

### Quick Test Commands

```bash
# Activate virtual environment first
source venv/bin/activate

# Run specific test file
pytest tests/blackjack/test_controller.py -v

# Run specific test function
pytest tests/blackjack/test_controller.py::TestBlackjackController::test_hit_method -v

# Run tests matching pattern
pytest tests/ -k "test_player" -v

# Run tests with short traceback
pytest tests/ -v --tb=short

# Run tests and stop at first failure
pytest tests/ -x

# Run only failed tests from last run
pytest tests/ --lf
```
