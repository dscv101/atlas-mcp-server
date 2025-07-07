# ATLAS MCP Server - Python Implementation

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.10+-green.svg)](https://github.com/jlowin/fastmcp)
[![KuzuDB](https://img.shields.io/badge/KuzuDB-0.6+-orange.svg)](https://kuzudb.com/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

ATLAS (Adaptive Task & Logic Automation System) is a Python-based Model Context Protocol (MCP) server that enables LLM agents to manage projects, tasks, and knowledge through an embedded graph database.

## 🚀 Features

- **Project Management**: Create, organize, and track projects with dependencies
- **Task Management**: Manage tasks with priorities, assignments, and dependencies
- **Knowledge Management**: Store and organize knowledge with domain categorization
- **Unified Search**: Advanced search across all entities with fuzzy matching
- **Graph Database**: Embedded KuzuDB for high-performance graph operations
- **Multiple Transports**: Support for stdio and HTTP transports
- **No Docker Required**: Single-process deployment with embedded database
- **Type Safety**: Full type hints and mypy compatibility
- **High Performance**: Optimized for speed and memory efficiency

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client Layer                        │
│  (Claude Desktop, IDEs, Custom Clients)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │ MCP Protocol (stdio/HTTP)
┌─────────────────────▼───────────────────────────────────────┐
│                 FastMCP Server                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │    Tools    │ │  Resources  │ │      Context &          │ │
│  │             │ │             │ │    Middleware           │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │ Service Layer API
┌─────────────────────▼───────────────────────────────────────┐
│                 Service Layer                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │   Project   │ │    Task     │ │      Knowledge &        │ │
│  │   Service   │ │   Service   │ │    Search Services      │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │ Database API
┌─────────────────────▼───────────────────────────────────────┐
│                 KuzuDB Layer                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ Connection  │ │   Schema    │ │      Query Engine       │ │
│  │  Manager    │ │  Manager    │ │                         │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Requirements

- **Python**: 3.12 or higher
- **Package Manager**: uv (recommended) or pip
- **Operating System**: Windows, macOS, Linux

## 🛠️ Installation

### Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/dscv101/atlas-mcp-server.git
cd atlas-mcp-server

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/dscv101/atlas-mcp-server.git
cd atlas-mcp-server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## ⚙️ Configuration

Copy the example configuration file and customize:

```bash
cp .env.example .env
```

Key configuration options:

```bash
# Database
ATLAS_DATABASE__PATH="./atlas.db"

# MCP Transport
ATLAS_MCP__TRANSPORT="stdio"  # or "http"
ATLAS_MCP__HOST="127.0.0.1"
ATLAS_MCP__PORT=8000

# Logging
ATLAS_MCP__LOG_LEVEL="INFO"
```

## 🚀 Usage

### Command Line

```bash
# Start with stdio transport (default)
atlas-mcp-server

# Start with HTTP transport
atlas-mcp-server --transport http --port 8000

# Initialize database
atlas-mcp-server --init-db

# Show help
atlas-mcp-server --help
```

### MCP Client Configuration

For stdio transport:
```json
{
  "mcpServers": {
    "atlas-mcp-server": {
      "command": "atlas-mcp-server",
      "args": [],
      "env": {
        "ATLAS_DATABASE__PATH": "/path/to/atlas.db"
      }
    }
  }
}
```

## 🧪 Development

### Setup Development Environment

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
ruff check .
ruff format .

# Run type checking
mypy src/
```

### Project Structure

```
src/atlas_mcp/
├── __init__.py          # Package initialization
├── main.py              # Main entry point
├── config/              # Configuration management
├── database/            # KuzuDB integration
├── models/              # Pydantic data models
├── services/            # Business logic services
├── tools/               # MCP tools implementation
├── resources/           # MCP resources implementation
└── utils/               # Utility functions

tests/                   # Test suite
├── conftest.py          # Test configuration
├── test_models/         # Model tests
├── test_services/       # Service tests
├── test_tools/          # Tool tests
└── test_integration/    # Integration tests
```

## 📊 Performance

Target performance metrics:
- **Tool Calls**: < 100ms for simple operations, < 500ms for complex operations
- **Resource Requests**: < 50ms for cached data, < 200ms for database queries
- **Memory Usage**: < 50MB base, < 200MB working, < 500MB peak
- **Scalability**: 10+ concurrent connections, 1GB+ databases

## 🔄 Migration from TypeScript

See [migration-guide.md](migration-guide.md) for detailed migration instructions from the TypeScript/Neo4j implementation.

## 📚 Documentation

- [Technical Specifications](tech-specs.md)
- [Implementation Plan](implementation-plan.md)
- [Migration Guide](migration-guide.md)
- [API Documentation](docs/) (Coming soon)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP framework
- [KuzuDB](https://kuzudb.com/) for the embedded graph database
- [Pydantic](https://pydantic.dev/) for data validation
- Original TypeScript implementation contributors

---

**Status**: 🚧 Under Development (Phase 1: Foundation Setup)

This is the Python implementation of ATLAS MCP Server. For the current TypeScript implementation, see the main branch.
