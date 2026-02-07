"""Main menu bar app for MacOS NetStat."""

import rumps
import time
from typing import Optional

from network import check_connection, measure_latency, get_connection_info
from bandwidth import get_bandwidth, format_speed, reset_bandwidth_stats
from config import get_config
from history import get_history


# Status icons
STATUS_CONNECTED = "●"
STATUS_DISCONNECTED = "○"

# Color indicators (rumps doesn't support true colors in title, using emoji-style)
COLOR_GREEN = "●"
COLOR_YELLOW = "●"
COLOR_RED = "○"


class NetStatApp(rumps.App):
    """Menu bar app for network status monitoring."""

    def __init__(self):
        """Initialize the app."""
        super().__init__(
            name="NetStat",
            icon=None,
            title=STATUS_DISCONNECTED,
            quit_button=None
        )

        # Load config
        self.config = get_config()
        self.history = get_history()

        # State tracking
        self.is_connected = False
        self.current_latency = None
        self.is_paused = False
        self.last_check_time = None

        # Build menu
        self._build_menu()

        # Start monitoring
        self.start_monitoring()

    def _build_menu(self):
        """Build the menu items."""
        # Status info items (will be updated dynamically)
        self.menu_status = rumps.MenuItem(f"Status: {STATUS_DISCONNECTED} Disconnected")
        self.menu_latency = rumps.MenuItem("Ping: --")
        self.menu_bandwidth = rumps.MenuItem("Bandwidth: --")

        # Connection info
        self.menu_connection = rumps.MenuItem("Connection: --")

        # Last check time
        self.menu_last_check = rumps.MenuItem("Last check: Never")

        # Separator
        self.menu.clear()

        # Add info items
        self.menu.add(self.menu_status)
        self.menu.add(self.menu_latency)
        self.menu.add(self.menu_bandwidth)
        self.menu.add(self.menu_connection)
        self.menu.add(self.menu_last_check)

        # Separator
        self.menu.add(rumps.separator)

        # History
        self.menu_history = rumps.MenuItem("📊 View History")
        self.menu_history.set_callback(self.show_history)
        self.menu.add(self.menu_history)

        # Settings
        self.menu_settings = rumps.MenuItem("⚙️ Settings...")
        self.menu_settings.set_callback(self.show_settings)
        self.menu.add(self.menu_settings)

        # Separator
        self.menu.add(rumps.separator)

        # Refresh button
        self.menu_refresh = rumps.MenuItem("🔄 Refresh Now")
        self.menu_refresh.set_callback(self.refresh_now)
        self.menu.add(self.menu_refresh)

        # Pause/Resume button
        self.menu_pause = rumps.MenuItem("⏸️ Pause Monitoring")
        self.menu_pause.set_callback(self.toggle_pause)
        self.menu.add(self.menu_pause)

        # Separator
        self.menu.add(rumps.separator)

        # Quit button
        self.menu_quit = rumps.MenuItem("❌ Quit")
        self.menu_quit.set_callback(self.quit_app)
        self.menu.add(self.menu_quit)

    def start_monitoring(self):
        """Start the monitoring timer."""
        interval = self.config.get("check_interval", 5)
        rumps.Timer(self.check_status, interval).start()

        # Initialize bandwidth stats
        if self.config.get("bandwidth_enabled", True):
            reset_bandwidth_stats()

    def check_status(self, sender):
        """Check network status and update UI.

        Args:
            sender: The timer that triggered this check.
        """
        if self.is_paused:
            return

        self.last_check_time = time.time()

        # Check connection and latency
        was_connected = self.is_connected
        self.is_connected = check_connection()

        # Handle connection state change
        if was_connected != self.is_connected:
            self._handle_state_change()

        # Get latency if connected
        if self.is_connected:
            self.current_latency = measure_latency()
        else:
            self.current_latency = None

        # Update UI
        self._update_ui()

    def _handle_state_change(self):
        """Handle connection state change (log and notify)."""
        if self.is_connected:
            # Connected
            latency = measure_latency()
            info = get_connection_info()
            details = f"{info.get('type', 'Unknown')}"
            if info.get('ssid'):
                details += f" - {info['ssid']}"

            self.history.log_event("connected", latency=latency, details=details)

            if self.config.get("notifications_enabled", True):
                rumps.notification(
                    title="Internet Connected",
                    subtitle=f"Latency: {latency}ms" if latency else "Connected",
                    message=details,
                    sound=True
                )
        else:
            # Disconnected
            self.history.log_event("disconnected", details="Connection lost")

            if self.config.get("notifications_enabled", True):
                rumps.notification(
                    title="Internet Disconnected",
                    subtitle="No internet connection",
                    message="Please check your network settings",
                    sound=True
                )

    def _update_ui(self):
        """Update the menu bar UI with current status."""
        # Update title
        if self.is_connected:
            if self.current_latency and self.current_latency >= 100:
                self.title = COLOR_YELLOW  # Slow
            else:
                self.title = COLOR_GREEN  # Good
        else:
            self.title = COLOR_RED  # Disconnected

        # Update status
        status_text = "Connected" if self.is_connected else "Disconnected"
        status_icon = STATUS_CONNECTED if self.is_connected else STATUS_DISCONNECTED
        self.menu_status.title = f"Status: {status_icon} {status_text}"

        # Update latency
        if self.current_latency is not None:
            self.menu_latency.title = f"Ping: {self.current_latency}ms"
        else:
            self.menu_latency.title = "Ping: --"

        # Update bandwidth if enabled
        if self.config.get("bandwidth_enabled", True):
            download, upload = get_bandwidth()
            down_str = format_speed(download)
            up_str = format_speed(upload)
            self.menu_bandwidth.title = f"↓ {down_str}  ↑ {up_str}"
        else:
            self.menu_bandwidth.title = "Bandwidth: Disabled"

        # Update connection info
        if self.is_connected:
            info = get_connection_info()
            conn_str = info.get("type", "Unknown")
            if info.get('ssid'):
                conn_str += f" ({info['ssid']})"
            self.menu_connection.title = f"Connection: {conn_str}"
        else:
            self.menu_connection.title = "Connection: --"

        # Update last check time
        if self.last_check_time:
            elapsed = int(time.time() - self.last_check_time)
            if elapsed < 60:
                self.menu_last_check.title = f"Updated {elapsed}s ago"
            else:
                mins = elapsed // 60
                self.menu_last_check.title = f"Updated {mins}m ago"

    def refresh_now(self, sender):
        """Force a refresh of network status.

        Args:
            sender: The menu item that triggered this action.
        """
        self.check_status(None)
        rumps.alert(
            title="Refresh Complete",
            message=f"Status: {'Connected' if self.is_connected else 'Disconnected'}",
            ok="OK"
        )

    def toggle_pause(self, sender):
        """Toggle pause/resume of monitoring.

        Args:
            sender: The menu item that triggered this action.
        """
        self.is_paused = not self.is_paused
        if self.is_paused:
            sender.title = "▶️ Resume Monitoring"
            self.title = "⏸️"
        else:
            sender.title = "⏸️ Pause Monitoring"
            self.check_status(None)

    def show_history(self, sender):
        """Show connection history.

        Args:
            sender: The menu item that triggered this action.
        """
        history_text = self.history.get_formatted_history(limit=50)
        stats = self.history.get_stats()

        stats_text = f"\n\nStats: {stats['total_events']} events, "
        if stats['average_latency']:
            stats_text += f"avg latency: {stats['average_latency']:.0f}ms"
        else:
            stats_text += "no latency data"

        rumps.alert(
            title="Connection History",
            message=history_text + stats_text,
            ok="Close"
        )

    def show_settings(self, sender):
        """Show and edit settings.

        Args:
            sender: The menu item that triggered this action.
        """
        # Create settings window
        response = rumps.Window(
            message="Enter check interval (1-60 seconds):",
            title="Settings",
            default=str(self.config.get("check_interval", 5)),
            ok="Save",
            cancel="Cancel"
        ).run()

        if response.clicked:
            try:
                interval = int(response.text)
                if 1 <= interval <= 60:
                    self.config.set("check_interval", interval)
                    rumps.alert(
                        title="Settings Saved",
                        message=f"Check interval set to {interval} seconds.\n\nRestart app to apply.",
                        ok="OK"
                    )
                else:
                    rumps.alert(
                        title="Invalid Value",
                        message="Please enter a value between 1 and 60.",
                        ok="OK"
                    )
            except ValueError:
                rumps.alert(
                    title="Invalid Value",
                    message="Please enter a valid number.",
                    ok="OK"
                )

    def quit_app(self, sender):
        """Quit the application.

        Args:
            sender: The menu item that triggered this action.
        """
        rumps.quit_application()


def main():
    """Main entry point."""
    app = NetStatApp()
    app.run()


if __name__ == "__main__":
    main()
