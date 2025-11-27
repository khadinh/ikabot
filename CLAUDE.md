# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ikabot is a cross-platform Python program that enhances the Ikariam game by offering premium features for free, focusing on city management, warfare strategies, and streamlined alerts. It's a console application with a modular architecture.

## Development Commands

### Setup and Installation
```bash
# Install in development mode
python -m pip install -e .

# Install test dependencies
pip install pytest pytest-mock
```

### Testing
```bash
# Run all tests
python -m pytest tests/ikabot

# Run specific test file
python -m pytest tests/ikabot/function/test_distributeResources.py
```

### Running the Application
```bash
# Run ikabot main application
python -m ikabot

# Run with direct module execution
python -m ikabot.command_line
```

### Code Formatting
- Use Black formatter for consistent code formatting (required per contribution guidelines)
- Format before submitting PRs

## Architecture

### Core Structure
- `ikabot/` - Main package directory
  - `command_line.py` - Entry point and main CLI interface
  - `config.py` - Global configuration, constants, and version management
  - `function/` - Core game automation modules (39+ specialized functions)
  - `helpers/` - Utility functions and common operations
  - `web/` - Web session management and HTTP operations
  - `locale/` - Internationalization support

### Key Components
- **Function Modules**: Each game feature is implemented as a separate module in `ikabot/function/`
  - Examples: `autoBarbarians.py`, `buyResources.py`, `donationBot.py`, `distributeResources.py`
  - Functions follow a consistent pattern for game automation tasks
- **Session Management**: `ikabot/web/session.py` handles game session state and HTTP requests
- **Configuration**: Centralized in `config.py` with game constants, API endpoints, and debug flags

### Testing Strategy
- Uses pytest framework
- Test files mirror the source structure: `tests/ikabot/function/`
- API-specific tests in `tests/api/`
- Focus on core functionality like resource distribution and game mechanics

## Development Guidelines

### Code Style
- **Lightweight Design Philosophy**: Prioritize functionality over unnecessary features
- **Minimal Dependencies**: Limit external dependencies (current: requests, cryptography, psutil, flask for web server)
- **Python Version**: Use latest Python versions (CI tests 3.9-3.12)
- **Formatting**: Use Black formatter (required)

### Project Conventions
- Version managed in `ikabot/config.py` (`IKABOT_VERSION`)
- Entry point: `ikabot.command_line:main`
- Debug flags available in config for development (`debugON_*` variables)
- Game constants and mappings centralized in config

### Contributing
- Keep PRs small and focused on single features
- Include screenshots for UI changes
- Unit tests encouraged but not mandatory
- Follow existing code patterns and conventions
- Check contribution guidelines in `.github/CONTRIBUTING.md`
