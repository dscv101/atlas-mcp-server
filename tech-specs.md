# ATLAS MCP Server - Technical Specifications

This document provides detailed technical requirements, dependencies, and design decisions for the Python implementation of ATLAS using FastMCP and KuzuDB.

## System Architecture

### High-Level Architecture

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

### Component Responsibilities

#### FastMCP Server Layer
- **MCP Protocol Handling**: Manages stdio and HTTP transports
- **Tool Registration**: Registers and routes MCP tool calls
- **Resource Management**: Handles MCP resource requests
- **Context Injection**: Provides request context and logging
- **Authentication**: Manages optional authentication for HTTP transport

#### Service Layer
- **Business Logic**: Implements core ATLAS functionality
- **Data Validation**: Validates input data and business rules
- **Transaction Management**: Manages database transactions
- **Error Handling**: Provides consistent error responses
- **Caching**: Implements caching for performance optimization

#### KuzuDB Layer
- **Data Persistence**: Stores and retrieves graph data
- **Query Execution**: Executes Cypher queries efficiently
- **Schema Management**: Maintains database schema and constraints
- **Backup/Restore**: Handles data export and import operations

## Technology Stack

### Core Dependencies

#### Python Runtime
- **Version**: Python 3.11+ (for modern type hints and performance)
- **Package Manager**: uv (for fast dependency resolution and virtual environments)
- **Build System**: pyproject.toml with setuptools backend

#### FastMCP Framework
- **Version**: FastMCP v2.x (latest stable)
- **Features Used**:
  - Tool decorators (@mcp.tool)
  - Resource decorators (@mcp.resource)
  - Context injection
  - Multiple transport support
  - Built-in authentication

#### KuzuDB Database
- **Version**: Latest stable release
- **Python Client**: kuzu package
- **Features Used**:
  - Embedded database (no server required)
  - Cypher query language
  - ACID transactions
  - Schema constraints
  - Graph algorithms

#### Supporting Libraries
```toml
[dependencies]
fastmcp = "^2.10.0"
kuzu = "^0.6.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
structlog = "^23.2.0"
click = "^8.1.0"
rich = "^13.7.0"
httpx = "^0.26.0"
asyncio-mqtt = "^0.16.0"  # For future MQTT transport
uvloop = "^0.19.0"  # For performance on Unix systems

[dev-dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.23.0"
pytest-cov = "^4.1.0"
pytest-mock = "^3.12.0"
ruff = "^0.1.0"
black = "^23.12.0"
mypy = "^1.8.0"
mkdocs = "^1.5.0"
mkdocs-material = "^9.5.0"
```

## Data Models

### Entity Definitions

#### Project Model
```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class URLReference(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    url: str = Field(..., regex=r'^https?://.+')

class Project(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    status: ProjectStatus = ProjectStatus.ACTIVE
    urls: Optional[List[URLReference]] = None
    completion_requirements: str = Field(..., min_length=1)
    output_format: str = Field(..., min_length=1)
    task_type: str = Field(..., min_length=1, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### Task Model
```python
class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    project_id: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    assigned_to: Optional[str] = None
    urls: Optional[List[URLReference]] = None
    tags: Optional[List[str]] = None
    completion_requirements: str = Field(..., min_length=1)
    output_format: str = Field(..., min_length=1)
    task_type: str = Field(..., min_length=1, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### Knowledge Model
```python
class Knowledge(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    project_id: str = Field(..., min_length=1, max_length=50)
    text: str = Field(..., min_length=1)
    tags: Optional[List[str]] = None
    domain: str = Field(..., min_length=1, max_length=100)
    citations: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Database Schema

#### KuzuDB Schema Definition
```cypher
-- Node Tables
CREATE NODE TABLE Project(
    id STRING,
    name STRING,
    description STRING,
    status STRING,
    urls STRING,  -- JSON serialized
    completion_requirements STRING,
    output_format STRING,
    task_type STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE NODE TABLE Task(
    id STRING,
    project_id STRING,
    title STRING,
    description STRING,
    priority STRING,
    status STRING,
    urls STRING,  -- JSON serialized
    tags STRING,  -- JSON serialized
    completion_requirements STRING,
    output_format STRING,
    task_type STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE NODE TABLE Knowledge(
    id STRING,
    project_id STRING,
    text STRING,
    tags STRING,  -- JSON serialized
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE NODE TABLE User(
    id STRING,
    username STRING,
    display_name STRING,
    email STRING,
    created_at TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE NODE TABLE Domain(
    name STRING,
    description STRING,
    PRIMARY KEY(name)
);

CREATE NODE TABLE Citation(
    id STRING,
    source STRING,
    title STRING,
    author STRING,
    date STRING,
    created_at TIMESTAMP,
    PRIMARY KEY(id)
);

-- Relationship Tables
CREATE REL TABLE CONTAINS_TASK(FROM Project TO Task);
CREATE REL TABLE CONTAINS_KNOWLEDGE(FROM Project TO Knowledge);
CREATE REL TABLE DEPENDS_ON(FROM Project TO Project);
CREATE REL TABLE TASK_DEPENDS_ON(FROM Task TO Task);
CREATE REL TABLE ASSIGNED_TO(FROM Task TO User);
CREATE REL TABLE BELONGS_TO_DOMAIN(FROM Knowledge TO Domain);
CREATE REL TABLE CITES(FROM Knowledge TO Citation);
```

## Service Layer Design

### Service Interface Pattern
```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class ServiceResult(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseService(ABC):
    def __init__(self, db_manager: 'DatabaseManager'):
        self.db = db_manager

    @abstractmethod
    async def create(self, entity: BaseModel) -> ServiceResult:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> ServiceResult:
        pass

    @abstractmethod
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> ServiceResult:
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> ServiceResult:
        pass

    @abstractmethod
    async def list_all(self, filters: Optional[Dict[str, Any]] = None) -> ServiceResult:
        pass
```

### Database Manager
```python
import kuzu
from typing import Optional, List, Dict, Any
import asyncio
from contextlib import asynccontextmanager

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db: Optional[kuzu.Database] = None
        self.conn: Optional[kuzu.Connection] = None

    async def initialize(self):
        """Initialize database connection and schema"""
        self.db = kuzu.Database(self.db_path)
        self.conn = kuzu.Connection(self.db)
        await self._create_schema()

    async def _create_schema(self):
        """Create database schema if not exists"""
        # Schema creation logic here
        pass

    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions"""
        try:
            self.conn.begin_transaction()
            yield self.conn
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return results"""
        result = self.conn.execute(query, params or {})
        return [dict(record) for record in result]

    async def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
        if self.db:
            self.db.close()
```

## Configuration Management

### Settings Schema
```python
from pydantic_settings import BaseSettings
from typing import Optional, List
from pathlib import Path

class DatabaseSettings(BaseSettings):
    path: Path = Path("./atlas.db")
    backup_dir: Path = Path("./backups")
    max_backups: int = 10
    auto_backup: bool = True
    backup_interval_hours: int = 24

class MCPSettings(BaseSettings):
    transport: str = "stdio"  # stdio, http, sse
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"
    auth_required: bool = False
    auth_secret_key: Optional[str] = None
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

class Settings(BaseSettings):
    app_name: str = "ATLAS MCP Server"
    app_version: str = "3.0.0"
    environment: str = "development"

    database: DatabaseSettings = DatabaseSettings()
    mcp: MCPSettings = MCPSettings()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
```

## Performance Specifications

### Response Time Requirements
- **Tool Calls**: < 100ms for simple operations, < 500ms for complex operations
- **Resource Requests**: < 50ms for cached data, < 200ms for database queries
- **Search Operations**: < 300ms for basic search, < 1000ms for complex search
- **Bulk Operations**: < 2000ms for up to 100 entities

### Memory Usage Targets
- **Base Memory**: < 50MB at startup
- **Working Memory**: < 200MB under normal load
- **Peak Memory**: < 500MB during bulk operations
- **Memory Growth**: < 1MB/hour during continuous operation

### Scalability Targets
- **Concurrent Connections**: Support 10+ simultaneous MCP clients
- **Database Size**: Handle databases up to 1GB efficiently
- **Entity Count**: Support 100K+ projects, 1M+ tasks, 10M+ knowledge items
- **Query Performance**: Maintain sub-second response times up to target scale

This technical specification provides the foundation for implementing a high-performance, scalable Python version of ATLAS while maintaining full compatibility with the existing TypeScript implementation.
