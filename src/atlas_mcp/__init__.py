"""
ATLAS MCP Server - Python Implementation

ATLAS (Adaptive Task & Logic Automation System) is a Model Context Protocol (MCP) server
that enables LLM agents to manage projects, tasks, and knowledge through a graph database.

This Python implementation uses FastMCP and KuzuDB to provide:
- Project, task, and knowledge management
- Unified search capabilities
- Backup and restore functionality
- Multiple transport support (stdio, HTTP)
- High performance with embedded graph database

Version: 3.0.0
License: Apache-2.0
"""

__version__ = "3.0.0"
__author__ = "cyanheads"
__email__ = "casey@caseyjhand.com"
__license__ = "Apache-2.0"

# Export main components
from atlas_mcp.main import main

__all__ = ["main", "__version__"]
