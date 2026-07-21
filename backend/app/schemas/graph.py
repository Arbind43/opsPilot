"""
OpsPilot — Graph Schemas
===========================
Schemas for Knowledge Graph exploration API.
"""

from typing import Any, List
from uuid import UUID

from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    label: str  # Node type (Equipment, Document, Incident, etc.)
    properties: dict[str, Any] = {}


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str
    properties: dict[str, Any] = {}


class GraphExploreResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class GraphSearchRequest(BaseModel):
    query: str
    node_types: List[str] | None = None
    limit: int = 50


class GraphPathRequest(BaseModel):
    source_id: str
    target_id: str
    max_depth: int = 5
