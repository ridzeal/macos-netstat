"""Connection history logging for MacOS NetStat."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# History file paths
CONFIG_DIR = Path.home() / ".macos-netstat"
HISTORY_FILE = CONFIG_DIR / "history.json"
MAX_HISTORY_ENTRIES = 100  # Keep last 100 events


class HistoryLogger:
    """Logger for connection state changes."""

    def __init__(self, max_entries: int = MAX_HISTORY_ENTRIES):
        """Initialize the history logger.

        Args:
            max_entries: Maximum number of history entries to keep.
        """
        self.max_entries = max_entries
        self._history: List[Dict] = []
        self._ensure_dir()
        self.load()

    def _ensure_dir(self):
        """Create config directory if it doesn't exist."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[Dict]:
        """Load history from file.

        Returns:
            List of history entries.
        """
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r") as f:
                    self._history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._history = []
        else:
            self._history = []
        return self._history

    def save(self) -> bool:
        """Save history to file.

        Returns:
            True if saved successfully, False otherwise.
        """
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump(self._history, f, indent=2)
            return True
        except IOError:
            return False

    def log_event(self, event_type: str, latency: Optional[int] = None, details: Optional[str] = None):
        """Log a connection event.

        Args:
            event_type: Type of event ("connected", "disconnected", etc.)
            latency: Latency in ms at time of event (optional).
            details: Additional details about the event (optional).
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
        }

        if latency is not None:
            entry["latency"] = latency

        if details is not None:
            entry["details"] = details

        self._history.append(entry)

        # Trim to max entries
        if len(self._history) > self.max_entries:
            self._history = self._history[-self.max_entries:]

        self.save()

    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get history entries.

        Args:
            limit: Maximum number of entries to return (most recent first).

        Returns:
            List of history entries.
        """
        if limit:
            return list(reversed(self._history[-limit:]))
        return list(reversed(self._history))

    def get_formatted_history(self, limit: int = 20) -> str:
        """Get formatted history as a readable string.

        Args:
            limit: Maximum number of entries to include.

        Returns:
            Formatted string with history entries.
        """
        entries = self.get_history(limit)

        if not entries:
            return "No history yet."

        lines = ["Connection History:", "-" * 40]

        for entry in entries:
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            event = entry["event"].capitalize()

            parts = [f"[{timestamp}] {event}"]

            if "latency" in entry:
                parts.append(f"({entry['latency']}ms)")

            if "details" in entry:
                parts.append(f"- {entry['details']}")

            lines.append(" ".join(parts))

        return "\n".join(lines)

    def clear(self) -> bool:
        """Clear all history.

        Returns:
            True if saved successfully, False otherwise.
        """
        self._history = []
        return self.save()

    def get_stats(self) -> Dict:
        """Get statistics about connection history.

        Returns:
            Dict with connection statistics.
        """
        connected_count = sum(1 for e in self._history if e["event"] == "connected")
        disconnected_count = sum(1 for e in self._history if e["event"] == "disconnected")

        # Calculate average latency
        latencies = [e.get("latency") for e in self._history if "latency" in e and e["latency"] is not None]
        avg_latency = sum(latencies) / len(latencies) if latencies else None

        return {
            "total_events": len(self._history),
            "connected_count": connected_count,
            "disconnected_count": disconnected_count,
            "average_latency": avg_latency,
        }


# Global history instance
_history_logger = None


def get_history() -> HistoryLogger:
    """Get the global history logger instance.

    Returns:
        The HistoryLogger singleton instance.
    """
    global _history_logger
    if _history_logger is None:
        _history_logger = HistoryLogger()
    return _history_logger


if __name__ == "__main__":
    # Test the history module
    print("Testing history module...")

    history = get_history()
    history.clear()

    # Log some test events
    history.log_event("connected", latency=25, details="WiFi - HomeNetwork")
    history.log_event("disconnected", details="Network unavailable")

    print(history.get_formatted_history())
    print(f"\nStats: {history.get_stats()}")
