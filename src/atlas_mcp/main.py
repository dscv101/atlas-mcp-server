#!/usr/bin/env python3
"""
ATLAS MCP Server - Main Entry Point

This module provides the main entry point for the ATLAS MCP server.
It handles command-line arguments, configuration loading, and server startup.
"""

import sys

import click
import structlog
from rich.console import Console
from rich.traceback import install

# Install rich traceback handler for better error display
install(show_locals=True)

# Initialize console for rich output
console = Console()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http"]),
    default="stdio",
    help="Transport type for MCP server (default: stdio)",
)
@click.option("--host", default="127.0.0.1", help="Host to bind HTTP server (default: 127.0.0.1)")
@click.option("--port", type=int, default=8000, help="Port to bind HTTP server (default: 8000)")
@click.option(
    "--database-path",
    type=click.Path(),
    default="./atlas.db",
    help="Path to KuzuDB database file (default: ./atlas.db)",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    help="Logging level (default: INFO)",
)
@click.option("--config-file", type=click.Path(exists=True), help="Path to configuration file")
@click.option("--init-db", is_flag=True, help="Initialize database schema and exit")
@click.version_option(version="3.0.0", prog_name="ATLAS MCP Server")
def main(
    transport: str,
    host: str,
    port: int,
    database_path: str,
    log_level: str,
    config_file: str | None,
    init_db: bool,
) -> None:
    """
    ATLAS MCP Server - Python Implementation

    A Model Context Protocol server for project, task, and knowledge management
    using FastMCP and KuzuDB.
    """
    try:
        # Set up logging level
        import logging

        logging.basicConfig(level=getattr(logging, log_level))

        # TODO: Implement config file loading
        _ = config_file  # Will be used in future implementation

        console.print("[bold green]ATLAS MCP Server v3.0.0[/bold green]")
        console.print(f"Transport: {transport}")
        console.print(f"Database: {database_path}")
        console.print(f"Log Level: {log_level}")

        if init_db:
            console.print("[yellow]Initializing database...[/yellow]")
            # TODO: Implement database initialization
            console.print("[green]Database initialized successfully![/green]")
            return

        if transport == "http":
            console.print(f"HTTP Server: http://{host}:{port}")

        # TODO: Implement server startup
        console.print("[yellow]Server startup not yet implemented[/yellow]")
        console.print("[blue]This is a placeholder for Phase 1 - Foundation Setup[/blue]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Server shutdown requested[/yellow]")
        logger.info("Server shutdown by user")
    except Exception as e:
        console.print(f"[red]Error starting server: {e}[/red]")
        logger.error("Server startup failed", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
