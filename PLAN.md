# MacBook Internet Status Widget - Implementation Plan

## Project Overview
Create a macOS menu bar widget that monitors and displays internet connection status with full details (status, latency, bandwidth, history, notifications).

**Scope**: Personal use only
**Tech Stack**: Python + rumps (free, no Apple Developer account needed)

---

## Project Structure
```
mbp-netstat/
├── main.py              # Entry point with rumps app setup
├── network.py           # Network check & monitoring logic
├── bandwidth.py         # Bandwidth monitoring (psutil)
├── history.py           # Connection history logger
├── config.py            # Settings management (JSON)
├── requirements.txt     # Python dependencies
├── assets/              # Status icons (optional)
└── build.sh             # Build script for standalone .app
```

---

## Features to Implement

### 1. Core Network Monitoring (network.py)
- `check_connection()` - HTTP request to `https://www.google.com/generate_204`
- `measure_latency()` - Ping time in milliseconds
- `get_connection_type()` - Detect WiFi/Ethernet/None
- State tracking (connected/disconnected)

### 2. Bandwidth Monitoring (bandwidth.py)
- `get_current_speed()` - Upload/download in real-time using psutil
- Network interface stats monitoring
- Calculate speed deltas between checks

### 3. Menu Bar UI (main.py)
- **Menu Bar Icon**: Status indicator (● green / ● yellow / ● red)
- **Dropdown Menu**:
  - Status: "● Connected" or "○ Disconnected"
  - Latency: "Ping: 24ms"
  - Bandwidth: "↓ 5.2 MB/s  ↑ 1.1 MB/s"
  - Connection: WiFi (SSID name)
  - Last check: "Updated 2s ago"
  - Separator
  - [📊 View History] - Opens history window
  - [⚙️ Settings...] - Opens preferences
  - Separator
  - [🔄 Refresh Now]
  - [⏸️ Pause Monitoring]
  - [❌ Quit]

### 4. Connection History (history.py)
- Log connection state changes with timestamps
- Store: timestamp, event (connected/disconnected), latency, duration
- Save to `~/.mbp-netstat/history.json`
- Simple text popup showing recent events

### 5. Notifications
- macOS notification on connection loss
- macOS notification on connection restored
- Configurable (enable/disable in settings)
- Use `rumps.notification()`

### 6. Settings (config.py)
- Check interval slider (1-60 seconds, default: 5)
- Notifications toggle (default: on)
- Bandwidth monitoring toggle (default: on)
- Auto-start on login option
- Persist to `~/.mbp-netstat/config.json`

---

## Implementation Steps

### Step 1: Project Setup
```bash
cd /Users/riadhiaditya/Apps/mbp-netstat
python3 -m venv venv
source venv/bin/activate
pip install rumps requests psutil
```

Create:
- `requirements.txt` with dependencies
- `main.py` with basic rumps app skeleton
- Test: app runs in menu bar with basic menu

### Step 2: Network Monitoring Core (network.py)
```python
def check_connection() -> bool:
    # HTTP GET to https://www.google.com/generate_204
    # Return True if status == 204

def measure_latency() -> int:
    # Time the HTTP request
    # Return milliseconds

def get_connection_info() -> dict:
    # Get SSID, connection type, local IP
```

### Step 3: Bandwidth Monitoring (bandwidth.py)
```python
def get_bandwidth() -> tuple:
    # Use psutil.net_io_counters()
    # Calculate delta from last check
    # Return (download_speed, upload_speed) in MB/s
```

### Step 4: Build Menu Bar UI (main.py)
- Create rumps.App class
- Add status indicator as title
- Build menu items dynamically
- Update menu items every interval
- Handle menu item clicks

### Step 5: Settings System (config.py)
- Create default config dict
- Load/save to JSON
- Build settings window with rumps
- Apply settings immediately

### Step 6: History & Notifications (history.py)
- Log state changes
- Create history viewer window
- Add notification triggers

### Step 7: Build Standalone App
- Create `setup.py` for py2app
- Build: `python setup.py py2app`
- Copy .app to /Applications
- Add to login items

---

## Dependencies (requirements.txt)
```
rumps>=0.4.0
requests>=2.31.0
psutil>=5.9.0
```

---

## Status Colors
| Color | Condition |
|-------|-----------|
| ● Green | Connected, latency <100ms |
| ● Yellow | Connected, latency >=100ms |
| ○ Red | Disconnected |

---

## Files to Create
1. `main.py` - Main app (~150 lines)
2. `network.py` - Network checks (~50 lines)
3. `bandwidth.py` - Bandwidth monitoring (~40 lines)
4. `history.py` - History logging (~60 lines)
5. `config.py` - Settings management (~80 lines)
6. `requirements.txt` - Dependencies (~3 lines)
7. `setup.py` - py2app config (~20 lines)
8. `build.sh` - Build script (~10 lines)

---

## Verification
1. Run app: `python main.py`
2. Menu bar icon appears with status
3. Click to see dropdown with all info
4. Toggle WiFi - status updates
5. Open Settings - change interval
6. View History - see logged events
7. Build app: `./build.sh`
8. Copy to /Applications and test standalone

---

## Estimated Scope
- **Total lines of code**: ~400-500 lines
- **Number of files**: 8 files
- **Development phases**: 7 steps
