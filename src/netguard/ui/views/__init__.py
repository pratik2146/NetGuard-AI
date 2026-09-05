"""
Streamlit UI view controllers package for NetGuard AI.
"""

from .dashboard import render_dashboard_view
from .prediction import render_prediction_view
from .device_explorer import render_device_explorer_view
from .about import render_about_view

__all__ = [
    "render_dashboard_view",
    "render_prediction_view",
    "render_device_explorer_view",
    "render_about_view",
]
