"""
Pytest configuration and shared fixtures for ATLAS MCP Server tests.

This module provides common test fixtures and configuration for the test suite.
"""

from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def temp_db_path(tmp_path: Path) -> Generator[Path]:
    """Provide a temporary database path for testing."""
    db_path = tmp_path / "test_atlas.db"
    yield db_path
    # Cleanup is handled automatically by tmp_path


@pytest.fixture
def sample_project_data() -> dict:
    """Provide sample project data for testing."""
    return {
        "id": "test-project-1",
        "name": "Test Project",
        "description": "A test project for unit testing",
        "status": "active",
        "completion_requirements": "Complete all test cases",
        "output_format": "Test results",
        "task_type": "testing",
    }


@pytest.fixture
def sample_task_data() -> dict:
    """Provide sample task data for testing."""
    return {
        "id": "test-task-1",
        "project_id": "test-project-1",
        "title": "Test Task",
        "description": "A test task for unit testing",
        "priority": "medium",
        "status": "todo",
        "completion_requirements": "Pass all assertions",
        "output_format": "Test output",
        "task_type": "unit-test",
    }


@pytest.fixture
def sample_knowledge_data() -> dict:
    """Provide sample knowledge data for testing."""
    return {
        "id": "test-knowledge-1",
        "project_id": "test-project-1",
        "text": "This is test knowledge for unit testing",
        "domain": "testing",
        "tags": ["test", "knowledge", "sample"],
    }
