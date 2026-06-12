from typing import Any
from rich import print as rprint
from rich.table import Table
from dateutil import parser


def pretty_print(items: Any):
    """Pretty-print lists of model objects or generic values using Rich.

    If objects implement `to_dict()` the function will display a table.
    """
    if isinstance(items, list):
        if not items:
            rprint("[italic]No items found[/]")
            return
        # Try to inspect first item
        first = items[0]
        if hasattr(first, "to_dict"):
            cols = list(first.to_dict().keys())
            table = Table(*cols)
            for it in items:
                d = it.to_dict()
                table.add_row(*[str(d.get(c, "")) for c in cols])
            rprint(table)
            return
    rprint(items)


def parse_date(text: str | None) -> str | None:
    if not text:
        return None
    try:
        """Parse a free-form date and return ISO date string or None."""
        dt = parser.parse(text)
        return dt.date().isoformat()
    except Exception:
        return None
