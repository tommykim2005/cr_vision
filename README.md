# CR Vision

Real-time Clash Royale opponent tracker using YOLOv8 computer vision. Tracks enemy elixir count and card cycle without spectator delay by reading the game screen directly.

## Features

- **Troop Detection** - YOLOv8 model trained on 1000+ Clash Royale images detects deployed troops in real time
- **Spatial Tracking** - Grid-based bucketing confirms deployments across multiple frames to reduce false positives
- **Elixir Estimation** - Wall-clock based elixir regeneration tracking for the opponent
- **Card Cycle Tracking** - Tracks which cards the enemy has played and predicts what's likely in hand
- **Match Lifecycle** - Automatic state machine detects VS screen, match start, match end, and new matches

## Project Structure

```
CRVISION/
├── core/
│   ├── screen_capture.py    # Screen grabbing via mss
│   └── window_finder.py     # macOS window detection via Quartz
├── game/
│   ├── troop_detector.py    # YOLOv8 inference wrapper
│   ├── troop_tracker.py     # Multi-frame deployment confirmation
│   ├── enemy_tracker.py     # Elixir + card cycle tracking
│   ├── vs_detector.py       # VS screen template matching
│   ├── state_machine.py     # Match lifecycle state machine
│   └── troop_costs.py       # Elixir cost lookup table
├── models/                  # YOLOv8 weights (not tracked in git)
├── images/                  # Template images (VS icon, etc.)
├── main.py                  # Application entry point
└── requirements.txt
```

## Requirements

- Python 3.10+
- macOS (uses Quartz for window detection)
- BlueStacks (or another Android emulator running Clash Royale)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Place your YOLOv8 model weights in `models/` (e.g. `models/bestv2.pt`).

## Usage

1. Open BlueStacks with Clash Royale running
2. Run the tracker:

```bash
python main.py
```

3. The tracker will automatically detect when a match starts and begin tracking
4. Press `q` to quit

## How It Works

1. **Screen Capture** - Grabs frames from the BlueStacks window using `mss`
2. **State Machine** - Detects match phases via VS screen template matching
3. **Detection** - Runs YOLOv8 inference on each frame during gameplay
4. **Tracking** - Confirms troop deployments by requiring consistent detections across multiple frames in the same grid region
5. **Elixir Model** - Estimates enemy elixir using wall-clock time regeneration (1 elixir per 2.8 seconds) minus known card costs
