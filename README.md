# MacOS NetStat

A macOS menu bar widget that monitors internet connection status with real-time updates.

## Features

- **Status Indicator**: Color-coded icon in menu bar (green/yellow/red)
- **Latency Measurement**: Real-time ping display in milliseconds
- **Bandwidth Monitoring**: Current upload/download speeds
- **Connection Info**: Shows connection type and WiFi SSID
- **Connection History**: Logs all connection state changes
- **Notifications**: Alerts on connection loss/restoration
- **Configurable Settings**: Adjustable check interval, toggles for features

## Installation

```bash
make install
```

## Usage

### Run the app

```bash
make run
```

### Build Standalone App

```bash
make build
```

### Other commands

```bash
make test   # Run module tests
make clean  # Clean build artifacts
make help   # Show all commands
```

Then copy `dist/NetStat.app` to `/Applications` and launch from there.

## Usage

1. Run the app - a status indicator appears in your menu bar
2. Click the indicator to see details:
   - Connection status
   - Ping latency
   - Bandwidth speeds
   - Connection type (WiFi/Ethernet)
3. Use the menu to:
   - View connection history
   - Change settings (check interval)
   - Pause/resume monitoring
   - Refresh status manually

## Configuration

Settings are stored in `~/.macos-netstat/config.json`:

```json
{
  "check_interval": 5,
  "notifications_enabled": true,
  "bandwidth_enabled": true,
  "auto_start": false
}
```

## Requirements

- macOS 10.13+
- Python 3.8+

## Dependencies

- `rumps` - Menu bar app framework
- `requests` - HTTP requests for connectivity checks
- `psutil` - System/network statistics

## Files

- `main.py` - Main application
- `network.py` - Network monitoring
- `bandwidth.py` - Bandwidth tracking
- `history.py` - Connection logging
- `config.py` - Settings management
- `setup.py` - py2app build config
- `build.sh` - Build script
