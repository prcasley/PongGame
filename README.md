# Pong Arcade

Modernized Pong with themes, polished UI, power-ups, difficulty levels, leaderboard persistence, and a CI-friendly headless test mode.

## Features

- Themes: Classic, Neon, Sunset with animated center net and accent colors
- Polished UI: Rounded buttons with hover, input boxes, Settings and Leaderboard screens
- Visual feedback: Ball trail, score pop animation, pause overlay, round-start countdown
- Game modes: 1 Player (vs CPU) and 2 Players (local)
- Difficulty: Easy, Normal, Hard (smarter CPU reactions and aim error tuning)
- Power-ups: Paddle Enlarge/Shrink, Ball Speed Up/Slow (timed effects)
- Controls: P1 `W/S` (or optional mouse), P2 `Up/Down`, Pause `P` or `Esc`
- Persistence: Leaderboard stored as `leaderboard.json` in the project directory
- Headless simulation: Non-interactive test mode for CI environments

## Requirements

- Python 3.8+
- pygame (pinned in `requirements.txt`)

Install options:

Option A: Virtual environment (recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Option B: User install
```bash
python3 -m pip install --user -r requirements.txt
```

## How to Play (Launch UI)

```bash
python3 Pong.py
```

- Enter names, choose 1 Player or 2 Players
- Use Settings for: Difficulty, Theme, Max Score, Power-Ups, P1 Mouse Control
- Leaderboard shows top players by wins; match results save on game over

### Controls

- P1: `W` / `S` (or enable mouse in Settings)
- P2: `Up` / `Down`
- Pause: `P` or `Esc`

## Headless Simulation (CI/Test)

Runs a fast, non-interactive match using the dummy video driver. Prints a single line on success.

```bash
PONG_HEADLESS_TEST=1 PONG_FAST_START=1 python3 Pong.py
```

Expected output contains:
```bash
TEST_RESULT <WinnerName> <LeftScore> <RightScore>
```

## Files

- `Pong.py`: Game source with UI, gameplay, settings, leaderboard, headless mode
- `requirements.txt`: Dependencies (pygame)
- `leaderboard.json`: Auto-created on first match end (do not edit while game is running)

## Notes & Troubleshooting

- Audio/ALSA warnings in headless runs are harmless and can be ignored in CI
- If `venv` creation fails on some systems, install your OS Python venv tools or use the user install option
- For fresh starts, you can delete `leaderboard.json`; it will be recreated automatically

## Changelog

Patch 1.1 (2025-09-15)
- Added themes, animated UI, Settings, Leaderboard with JSON persistence
- Added visual effects (trail, score pop), pause overlay, countdown
- Implemented difficulty levels for CPU and power-ups with timers
- Added headless simulation mode for CI
