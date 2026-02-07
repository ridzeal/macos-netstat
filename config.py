"""Configuration management for MacOS NetStat."""

import json
import os
from pathlib import Path
from typing import Any, Dict


# Default configuration values
DEFAULT_CONFIG = {
    "check_interval": 5,  # seconds
    "notifications_enabled": True,
    "bandwidth_enabled": True,
    "auto_start": False,
}


# Config directory and file paths
CONFIG_DIR = Path.home() / ".macos-netstat"
CONFIG_FILE = CONFIG_DIR / "config.json"


class Config:
    """Configuration manager for the app."""

    def __init__(self):
        """Initialize configuration with defaults and load from file if exists."""
        self._config = DEFAULT_CONFIG.copy()
        self._ensure_config_dir()
        self.load()

    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """Load configuration from file.

        Returns:
            The loaded configuration dict.
        """
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle new config keys
                    self._config = {**DEFAULT_CONFIG, **loaded}
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                self._config = DEFAULT_CONFIG.copy()
        return self._config

    def save(self) -> bool:
        """Save configuration to file.

        Returns:
            True if saved successfully, False otherwise.
        """
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self._config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key.
            default: Default value if key doesn't exist.

        Returns:
            The configuration value or default.
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """Set a configuration value and save to file.

        Args:
            key: Configuration key.
            value: Value to set.

        Returns:
            True if saved successfully, False otherwise.
        """
        self._config[key] = value
        return self.save()

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values.

        Returns:
            Dictionary of all configuration values.
        """
        return self._config.copy()

    def update(self, updates: Dict[str, Any]) -> bool:
        """Update multiple configuration values and save.

        Args:
            updates: Dictionary of key-value pairs to update.

        Returns:
            True if saved successfully, False otherwise.
        """
        self._config.update(updates)
        return self.save()

    def reset(self) -> bool:
        """Reset configuration to defaults and save.

        Returns:
            True if saved successfully, False otherwise.
        """
        self._config = DEFAULT_CONFIG.copy()
        return self.save()


# Global config instance
_config = None


def get_config() -> Config:
    """Get the global configuration instance.

    Returns:
        The Config singleton instance.
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


if __name__ == "__main__":
    # Test the config module
    print("Testing config module...")

    config = get_config()
    print(f"Config file: {CONFIG_FILE}")
    print(f"Current config: {config.get_all()}")

    # Test setting values
    config.set("check_interval", 10)
    print(f"After setting interval to 10: {config.get('check_interval')}")

    # Test reset
    config.reset()
    print(f"After reset: {config.get_all()}")
