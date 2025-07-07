# ATLAS MCP Server - Migration Guide

This document provides step-by-step instructions for migrating from the current TypeScript/Neo4j implementation to the new Python/FastMCP/KuzuDB implementation.

## Migration Overview

### What's Changing
- **Language**: TypeScript → Python 3.11+
- **MCP Framework**: @modelcontextprotocol/sdk → FastMCP v2.x
- **Database**: Neo4j → KuzuDB (embedded)
- **Deployment**: Docker Compose → Native Python process
- **Configuration**: Environment variables → Pydantic settings

### What's Staying the Same
- **MCP Protocol**: Full compatibility maintained
- **API Interface**: All 15 tools with identical signatures
- **Data Model**: Same 3-tier architecture (Projects, Tasks, Knowledge)
- **Resource URIs**: Identical resource patterns and templates
- **Functionality**: All features preserved including search and backup/restore

## Pre-Migration Checklist

### 1. Environment Assessment
- [ ] Verify current ATLAS version (should be 2.8.15 or compatible)
- [ ] Document current configuration settings
- [ ] Identify any custom modifications or integrations
- [ ] Test current backup/restore functionality
- [ ] Record performance baselines for comparison

### 2. Data Backup
- [ ] Create full database backup using current system
- [ ] Export data using `npm run db:backup`
- [ ] Verify backup integrity and completeness
- [ ] Store backup in secure location
- [ ] Document backup location and timestamp

### 3. Client Configuration Audit
- [ ] Document all MCP client configurations
- [ ] Identify transport types in use (stdio vs HTTP)
- [ ] Record authentication settings if using HTTP transport
- [ ] Note any custom client integrations

## Migration Process

### Phase 1: Preparation (Day 1)

#### 1.1 Install Python Environment
```bash
# Install Python 3.11+ if not already available
# On macOS with Homebrew
brew install python@3.11

# On Ubuntu/Debian
sudo apt update && sudo apt install python3.11 python3.11-venv

# On Windows
# Download from python.org or use Windows Store
```

#### 1.2 Install uv Package Manager
```bash
# Install uv for fast package management
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

#### 1.3 Download Python Implementation
```bash
# Clone or download the Python ATLAS implementation
git clone https://github.com/your-org/atlas-mcp-server-python.git
cd atlas-mcp-server-python

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Phase 2: Configuration Migration (Day 1)

#### 2.1 Convert Environment Variables
Create `.env` file based on current configuration:

```bash
# Current TypeScript config → Python config mapping

# Database settings
ATLAS_DATABASE__PATH=./atlas.db  # New: KuzuDB file path
# Remove: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# MCP settings (mostly unchanged)
ATLAS_MCP__TRANSPORT=stdio  # or http
ATLAS_MCP__HOST=127.0.0.1
ATLAS_MCP__PORT=3010
ATLAS_MCP__LOG_LEVEL=info

# Security settings (if using HTTP)
ATLAS_MCP__AUTH_REQUIRED=false
ATLAS_MCP__AUTH_SECRET_KEY=your_secret_key
ATLAS_MCP__RATE_LIMIT_REQUESTS=100
ATLAS_MCP__RATE_LIMIT_WINDOW_SECONDS=60

# Backup settings
ATLAS_DATABASE__BACKUP_DIR=./backups
ATLAS_DATABASE__MAX_BACKUPS=10
ATLAS_DATABASE__AUTO_BACKUP=true
```

#### 2.2 Update Client Configurations
Update MCP client configurations to point to Python implementation:

**For stdio transport:**
```json
{
  "mcpServers": {
    "atlas-mcp-server": {
      "command": "python",
      "args": ["/path/to/atlas-mcp-server-python/src/atlas_mcp/main.py"],
      "env": {
        "ATLAS_MCP__TRANSPORT": "stdio",
        "ATLAS_MCP__LOG_LEVEL": "info",
        "ATLAS_DATABASE__PATH": "/path/to/atlas.db"
      }
    }
  }
}
```

**For HTTP transport:**
```json
{
  "mcpServers": {
    "atlas-mcp-server": {
      "command": "python",
      "args": ["/path/to/atlas-mcp-server-python/src/atlas_mcp/main.py"],
      "env": {
        "ATLAS_MCP__TRANSPORT": "http",
        "ATLAS_MCP__HOST": "127.0.0.1",
        "ATLAS_MCP__PORT": "8000",
        "ATLAS_DATABASE__PATH": "/path/to/atlas.db"
      }
    }
  }
}
```

### Phase 3: Data Migration (Day 2)

#### 3.1 Export Data from Neo4j
Using the current TypeScript implementation:
```bash
# Ensure Neo4j is running
docker-compose up -d

# Export all data
npm run db:backup

# Verify export files exist
ls -la ./atlas-backups/atlas-backup-*/
# Should contain: projects.json, tasks.json, knowledge.json, relationships.json, full-export.json
```

#### 3.2 Import Data to KuzuDB
Using the new Python implementation:
```bash
# Initialize the Python server (creates empty KuzuDB)
python src/atlas_mcp/main.py --init-db

# Import data from Neo4j backup
python src/atlas_mcp/tools/migrate_data.py \
  --source ./atlas-backups/atlas-backup-YYYYMMDDHHMMSS/full-export.json \
  --target ./atlas.db

# Verify data import
python src/atlas_mcp/tools/verify_migration.py \
  --database ./atlas.db \
  --backup ./atlas-backups/atlas-backup-YYYYMMDDHHMMSS/
```

#### 3.3 Validate Data Integrity
```bash
# Run data validation checks
python src/atlas_mcp/tools/validate_data.py --database ./atlas.db

# Compare entity counts
python src/atlas_mcp/tools/compare_counts.py \
  --neo4j-backup ./atlas-backups/atlas-backup-YYYYMMDDHHMMSS/ \
  --kuzu-db ./atlas.db

# Test basic operations
python src/atlas_mcp/tools/test_operations.py --database ./atlas.db
```

### Phase 4: Testing and Validation (Day 2-3)

#### 4.1 Functional Testing
```bash
# Test MCP protocol compliance
python -m pytest tests/test_mcp_protocol.py -v

# Test all tools
python -m pytest tests/test_tools.py -v

# Test all resources
python -m pytest tests/test_resources.py -v

# Test search functionality
python -m pytest tests/test_search.py -v
```

#### 4.2 Performance Testing
```bash
# Run performance benchmarks
python src/atlas_mcp/tools/benchmark.py \
  --database ./atlas.db \
  --output ./performance_report.json

# Compare with baseline (if available)
python src/atlas_mcp/tools/compare_performance.py \
  --current ./performance_report.json \
  --baseline ./baseline_performance.json
```

#### 4.3 Integration Testing
```bash
# Test with actual MCP clients
# Start the server
python src/atlas_mcp/main.py

# In another terminal, test with mcp-inspector
mcp-inspector --config ./test_config.json

# Test specific operations
atlas_project_create --name "Test Migration" --description "Testing migration"
atlas_project_list
atlas_unified_search --value "migration"
```

### Phase 5: Deployment (Day 3)

#### 5.1 Stop Current Implementation
```bash
# Stop the TypeScript server
# If running as service, stop the service
sudo systemctl stop atlas-mcp-server

# If running with Docker
docker-compose down

# If running manually, stop the process
```

#### 5.2 Deploy Python Implementation
```bash
# Copy configuration
cp .env /opt/atlas-mcp-server-python/

# Copy database
cp atlas.db /opt/atlas-mcp-server-python/

# Install as system service (optional)
sudo cp scripts/atlas-mcp-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable atlas-mcp-server
sudo systemctl start atlas-mcp-server
```

#### 5.3 Update Client Configurations
Update all MCP clients to use the new Python implementation:
- Update command paths in client configurations
- Restart MCP clients
- Verify connectivity and functionality

## Post-Migration Verification

### 1. Functional Verification
- [ ] All 15 MCP tools respond correctly
- [ ] All MCP resources return expected data
- [ ] Search functionality works as expected
- [ ] Backup/restore operations function properly
- [ ] Authentication works (if enabled)

### 2. Performance Verification
- [ ] Response times meet or exceed previous performance
- [ ] Memory usage is within acceptable limits
- [ ] Database operations complete successfully
- [ ] No memory leaks during extended operation

### 3. Data Integrity Verification
- [ ] All projects migrated correctly
- [ ] All tasks migrated with proper relationships
- [ ] All knowledge items preserved
- [ ] User assignments maintained
- [ ] Dependencies preserved
- [ ] Metadata (timestamps, URLs, tags) intact

## Rollback Procedure

If issues are encountered, follow this rollback procedure:

### 1. Stop Python Implementation
```bash
sudo systemctl stop atlas-mcp-server
# or kill the Python process
```

### 2. Restore TypeScript Implementation
```bash
# Restart Neo4j
docker-compose up -d

# Restore from backup if needed
npm run db:import ./atlas-backups/atlas-backup-YYYYMMDDHHMMSS/

# Start TypeScript server
npm run start:stdio  # or start:http
```

### 3. Revert Client Configurations
- Restore original MCP client configurations
- Restart MCP clients
- Verify functionality

## Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database file permissions
ls -la atlas.db

# Verify database integrity
python src/atlas_mcp/tools/check_db.py --database ./atlas.db
```

#### Performance Issues
```bash
# Check system resources
htop
df -h

# Analyze query performance
python src/atlas_mcp/tools/analyze_queries.py --database ./atlas.db
```

#### MCP Protocol Issues
```bash
# Test MCP compliance
python src/atlas_mcp/tools/test_mcp.py

# Check logs
tail -f logs/atlas-mcp-server.log
```

### Getting Help
- Check the troubleshooting guide in the documentation
- Review logs for error messages
- Contact support with specific error details and system information

## Success Criteria

Migration is considered successful when:
- [ ] All functional tests pass
- [ ] Performance meets or exceeds baseline
- [ ] Data integrity is verified
- [ ] All MCP clients connect successfully
- [ ] No critical errors in logs after 24 hours of operation

This migration guide ensures a smooth transition from the TypeScript implementation to the new Python implementation while maintaining full functionality and data integrity.
