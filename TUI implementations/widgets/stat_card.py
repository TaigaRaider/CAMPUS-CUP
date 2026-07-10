"""
StatCard Widget

A reusable card widget for displaying a single statistic on the dashboard.
Shows a large numeric value with a descriptive label underneath.

Usage:
    yield StatCard("12", "Total Teams", variant="primary")
    yield StatCard("5", "Pending Matches")
    yield StatCard("8", "Active Matches", variant="success")
"""

from __future__ import annotations
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static


class StatCard(Widget):
    """A card displaying a statistic value and label.

    Args:
        value: The numeric/string value to display prominently.
        label: A short description of what the value represents.
        variant: Optional style variant — 'primary' (blue) or 'success' (green).
                 Defaults to standard green styling.
    """

    def __init__(self, value: str, label: str, variant: str = "", **kwargs):
        super().__init__(**kwargs)
        self._value = value
        self._label = label
        self._variant = variant

    def compose(self) -> ComposeResult:
        css_class = "stat-card"
        if self._variant:
            css_class += f" {self._variant}"

        with Vertical(classes=css_class):
            yield Static(self._value, classes="stat-value")
            yield Static(self._label, classes="stat-label")
