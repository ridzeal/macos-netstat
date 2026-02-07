"""Network monitoring module for checking internet connectivity and latency."""

import time
import socket
import subprocess
import requests
from typing import Tuple, Optional


# Test endpoint that returns 204 No Content (minimal data usage)
TEST_ENDPOINT = "https://www.google.com/generate_204"
TIMEOUT = 5  # seconds


def check_connection() -> bool:
    """Check if internet connection is available.

    Returns:
        True if connected, False otherwise.
    """
    try:
        response = requests.get(TEST_ENDPOINT, timeout=TIMEOUT)
        return response.status_code == 204
    except (requests.RequestException, OSError):
        return False


def measure_latency() -> Optional[int]:
    """Measure internet latency using HTTP request.

    Returns:
        Latency in milliseconds, or None if connection failed.
    """
    try:
        start = time.time()
        response = requests.get(TEST_ENDPOINT, timeout=TIMEOUT)
        end = time.time()

        if response.status_code == 204:
            return int((end - start) * 1000)
        return None
    except (requests.RequestException, OSError):
        return None


def get_connection_info() -> dict:
    """Get detailed connection information.

    Returns:
        Dict with connection type, SSID (if WiFi), and local IP.
    """
    info = {
        "type": "Unknown",
        "ssid": None,
        "local_ip": None,
    }

    # Try to get WiFi SSID (macOS only)
    try:
        result = subprocess.run(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "SSID:" in line and "BSSID" not in line:
                    info["ssid"] = line.split("SSID:")[1].strip()
                    info["type"] = "WiFi"
                    break
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Check for Ethernet if WiFi wasn't found
    if info["type"] == "Unknown":
        try:
            # Get network interfaces
            result = subprocess.run(
                ["ifconfig"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if "en0" in result.stdout:
                info["type"] = "Ethernet"
        except subprocess.TimeoutExpired:
            pass

    # Get local IP address
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        # Doesn't actually send data, just gets the routing interface
        s.connect(("8.8.8.8", 80))
        info["local_ip"] = s.getsockname()[0]
        s.close()
    except (OSError, socket.error):
        pass

    return info


def get_external_ip() -> Optional[str]:
    """Get the external IP address.

    Returns:
        External IP address, or None if unable to determine.
    """
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=TIMEOUT)
        return response.text.strip() if response.status_code == 200 else None
    except (requests.RequestException, OSError):
        return None


if __name__ == "__main__":
    # Test the functions
    print("Testing network module...")

    print("Checking connection...")
    is_connected = check_connection()
    print(f"Connected: {is_connected}")

    if is_connected:
        print(f"Latency: {measure_latency()}ms")

        info = get_connection_info()
        print(f"Connection info: {info}")

        print(f"External IP: {get_external_ip()}")
