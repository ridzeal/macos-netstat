"""Bandwidth monitoring module using psutil."""

import time
import psutil
from typing import Tuple, Optional


# Store previous stats for calculating speed
_prev_stats = {
    "bytes_sent": 0,
    "bytes_recv": 0,
    "timestamp": 0
}


def get_bandwidth(interval: float = 1.0) -> Tuple[Optional[float], Optional[float]]:
    """Get current download and upload speeds.

    Args:
        interval: Time in seconds between measurements. Default 1.0.

    Returns:
        Tuple of (download_speed, upload_speed) in MB/s.
        Returns (None, None) on first call or error.
    """
    global _prev_stats

    current_time = time.time()
    current_stats = psutil.net_io_counters()

    # First call - just store stats and return None
    if _prev_stats["timestamp"] == 0:
        _prev_stats = {
            "bytes_sent": current_stats.bytes_sent,
            "bytes_recv": current_stats.bytes_recv,
            "timestamp": current_time
        }
        return None, None

    # Calculate time delta
    time_delta = current_time - _prev_stats["timestamp"]

    # Avoid division by zero
    if time_delta == 0:
        return None, None

    # Calculate byte deltas
    sent_delta = current_stats.bytes_sent - _prev_stats["bytes_sent"]
    recv_delta = current_stats.bytes_recv - _prev_stats["bytes_recv"]

    # Handle counter reset (can happen on some systems)
    if sent_delta < 0 or recv_delta < 0:
        _prev_stats = {
            "bytes_sent": current_stats.bytes_sent,
            "bytes_recv": current_stats.bytes_recv,
            "timestamp": current_time
        }
        return None, None

    # Update previous stats
    _prev_stats = {
        "bytes_sent": current_stats.bytes_sent,
        "bytes_recv": current_stats.bytes_recv,
        "timestamp": current_time
    }

    # Calculate speeds in MB/s
    download_speed = (recv_delta / time_delta) / (1024 * 1024)
    upload_speed = (sent_delta / time_delta) / (1024 * 1024)

    return download_speed, upload_speed


def get_total_usage() -> Tuple[float, float]:
    """Get total data usage since boot.

    Returns:
        Tuple of (total_sent_GB, total_recv_GB).
    """
    stats = psutil.net_io_counters()
    total_sent_gb = stats.bytes_sent / (1024 ** 3)
    total_recv_gb = stats.bytes_recv / (1024 ** 3)
    return total_sent_gb, total_recv_gb


def reset_bandwidth_stats():
    """Reset bandwidth statistics (mainly for testing)."""
    global _prev_stats
    _prev_stats = {
        "bytes_sent": 0,
        "bytes_recv": 0,
        "timestamp": 0
    }


def format_speed(speed: Optional[float]) -> str:
    """Format speed for display.

    Args:
        speed: Speed in MB/s.

    Returns:
        Formatted string (e.g., "5.2 MB/s" or "N/A").
    """
    if speed is None:
        return "N/A"

    if speed < 1:
        return f"{speed * 1024:.1f} KB/s"
    return f"{speed:.2f} MB/s"


if __name__ == "__main__":
    # Test the functions
    print("Testing bandwidth module...")
    print("Waiting 2 seconds for initial reading...")

    # First call initializes stats
    get_bandwidth()

    time.sleep(2)

    download, upload = get_bandwidth()
    print(f"Download: {format_speed(download)}")
    print(f"Upload: {format_speed(upload)}")

    total_sent, total_recv = get_total_usage()
    print(f"Total sent: {total_sent:.2f} GB")
    print(f"Total received: {total_recv:.2f} GB")
