# ATLAS MCP Server - Architecture Analysis

This document provides a comprehensive analysis of the current ATLAS MCP server implementation to guide the migration to Python with FastMCP and KuzuDB.

## Executive Summary

ATLAS (Adaptive Task & Logic Automation System) is a TypeScript-based MCP server that provides project, task, and knowledge management capabilities for LLM agents. The current implementation uses Neo4j as the graph database and the official MCP SDK for protocol implementation.

### Current Architecture Overview

- **Language**: TypeScript/Node.js
- **MCP Framework**: @modelcontextprotocol/sdk v1.12.1
- **Database**: Neo4j v5 Community + APOC plugin
- **Transport**: Supports both stdio and HTTP
- **Deployment**: Docker Compose for Neo4j
- **Version**: 2.8.15 (stable)

## Core Components

### 1. Data Model (3-Tier Architecture)

```
PROJECT (top-level containers)
├── TASK (actionable items within projects)
├── KNOWLEDGE (information/context for projects)
└── DEPENDENCIES (relationships between entities)
```

#### Project Entity
- **Properties**: id, name, description, status, urls, completionRequirements, outputFormat, taskType, createdAt, updatedAt
- **Relationships**: CONTAINS_TASK, CONTAINS_KNOWLEDGE, DEPENDS_ON
- **Status Values**: active, completed, on_hold, cancelled

#### Task Entity
- **Properties**: id, projectId, title, description, priority, status, urls, tags, completionRequirements, outputFormat, taskType, createdAt, updatedAt
- **Relationships**: BELONGS_TO_PROJECT, ASSIGNED_TO (User), DEPENDS_ON
- **Priority Levels**: low, medium, high, urgent
- **Status Values**: todo, in_progress, completed, cancelled

#### Knowledge Entity
- **Properties**: id, projectId, text, tags, createdAt, updatedAt
- **Relationships**: BELONGS_TO_PROJECT, BELONGS_TO_DOMAIN, CITES
- **Domain**: Categorical organization of knowledge

### 2. MCP Server Implementation

#### Server Structure (`src/mcp/server.ts`)
- **Framework**: @modelcontextprotocol/sdk
- **Capabilities**: logging, resources (listChanged), tools (listChanged, requestContext, rateLimit, permissions)
- **Transport Support**: stdio (default), HTTP with SSE
- **Authentication**: Optional JWT-based auth for HTTP transport

#### Tools (15 total)
1. **Project Operations**: create, list, update, delete
2. **Task Operations**: create, list, update, delete
3. **Knowledge Operations**: add, list, delete
4. **Search Operations**: unified search across entities
5. **Research Operations**: deep research planning
6. **Database Operations**: clean (destructive reset)

#### Resources
- **Direct Resources**: `atlas://projects`, `atlas://tasks`, `atlas://knowledge`
- **Template Resources**: `atlas://projects/{projectId}`, `atlas://tasks/{taskId}`, etc.
- **Pagination Support**: All list operations support pagination

### 3. Neo4j Integration

#### Connection Management
- **Driver**: Singleton pattern with connection pooling
- **Configuration**: maxConnectionLifetime (3h), maxConnectionPoolSize (50), connectionAcquisitionTimeout (2min)
- **Session Management**: Write/read sessions with transaction support

#### Query Patterns
- **CRUD Operations**: Parameterized Cypher queries
- **Relationship Management**: MERGE operations for creating relationships
- **Complex Searches**: Property-based and full-text search with scoring
- **JSON Serialization**: Complex properties (URLs, tags) stored as JSON strings

#### Schema Management
- **Constraints**: Unique constraints on entity IDs
- **Indexes**: Primary key indexes for performance
- **Node Labels**: Project, Task, Knowledge, User, TaskType, Domain, Citation
- **Relationship Types**: CONTAINS_TASK, CONTAINS_KNOWLEDGE, DEPENDS_ON, ASSIGNED_TO, CITES, RELATED_TO, HAS_TYPE, BELONGS_TO_DOMAIN, BELONGS_TO_PROJECT

### 4. Service Layer Architecture

#### Core Services
- **ProjectService**: CRUD operations for projects
- **TaskService**: CRUD operations for tasks with user assignment
- **KnowledgeService**: CRUD operations for knowledge with domain relationships
- **SearchService**: Unified search across all entities
- **BackupRestoreService**: Database backup/restore functionality

#### Utility Services
- **Neo4jDriver**: Connection management and query execution
- **Neo4jUtils**: Schema initialization, validation, pagination
- **ErrorHandler**: Centralized error management
- **Logger**: Winston-based logging with request context
- **RequestContextService**: Request tracking and correlation

### 5. Configuration Management

#### Environment Variables
- **Neo4j**: URI, user, password
- **MCP**: transport type, HTTP host/port, log level
- **Security**: rate limiting, authentication (optional)
- **Backup**: max count, file directory

#### Validation
- **Schema**: Zod-based configuration validation
- **Defaults**: Comprehensive default values for all settings

## Key Features

### 1. Comprehensive CRUD Operations
- **Bulk Operations**: Support for creating/updating/deleting multiple entities
- **Validation**: Input validation with detailed error messages
- **Relationships**: Automatic relationship management
- **Metadata**: Rich metadata tracking (URLs, tags, timestamps)

### 2. Advanced Search Capabilities
- **Unified Search**: Cross-entity search with relevance scoring
- **Property-Based Search**: Regex search on specific properties
- **Full-Text Search**: Lucene-based full-text search
- **Fuzzy Matching**: Configurable fuzzy search options
- **Filtering**: Entity type, task type, assignment filters

### 3. Dependency Management
- **Project Dependencies**: Inter-project dependency tracking
- **Task Dependencies**: Task-to-task dependency relationships
- **Validation**: Circular dependency detection
- **Cascading Operations**: Dependency-aware operations

### 4. User Management
- **User Entities**: Username, display name, email
- **Task Assignment**: ASSIGNED_TO relationships
- **User Creation**: Automatic user creation on assignment

### 5. Backup and Restore
- **Export Format**: JSON files for each entity type
- **Full Export**: Complete database export in single file
- **Restore Process**: Complete database restoration from backup
- **Automation**: Configurable backup retention

### 6. Web UI (Experimental)
- **Visualization**: Basic project, task, and knowledge viewing
- **Static Files**: HTML/CSS/JS served via Express
- **API Integration**: Direct Neo4j API calls from frontend

## Technical Strengths

1. **Mature MCP Implementation**: Uses official SDK with full protocol support
2. **Robust Database Layer**: Neo4j provides ACID transactions and graph capabilities
3. **Comprehensive Feature Set**: Full CRUD, search, backup/restore, dependencies
4. **Production Ready**: Authentication, rate limiting, logging, error handling
5. **Flexible Transport**: Both stdio and HTTP support
6. **Rich Metadata**: Extensive property support for all entities

## Technical Challenges

1. **Docker Dependency**: Requires Docker for Neo4j deployment
2. **Complex Setup**: Multi-component architecture with external dependencies
3. **Resource Usage**: Neo4j requires significant memory and storage
4. **TypeScript Complexity**: Large codebase with complex type definitions
5. **Neo4j Licensing**: Community edition limitations for production use

## Migration Opportunities

1. **Simplified Deployment**: KuzuDB eliminates Docker requirement
2. **Embedded Database**: Single-process deployment model
3. **Python Ecosystem**: Better integration with AI/ML tools
4. **FastMCP Benefits**: Simplified MCP server development
5. **Performance**: KuzuDB offers better analytical performance
6. **Cost Reduction**: No Neo4j licensing costs

This analysis provides the foundation for planning the migration to Python with FastMCP and KuzuDB while maintaining all existing functionality and improving deployment simplicity.
