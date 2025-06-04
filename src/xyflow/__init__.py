"""xyflow - Beautiful network visualizations with xyflow."""

from __future__ import annotations

import importlib.metadata

from xyflow.data_types import Edge, Node, Props
from xyflow.nx import from_networkx
from xyflow.widget import XYFlowWidget

try:
    __version__ = importlib.metadata.version("xyflow")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


# What we export when users do `from xyflow import *`
__all__ = [
    "Edge",
    "Node",
    "Props",
    "XYFlowWidget",
    "from_networkx",
]
