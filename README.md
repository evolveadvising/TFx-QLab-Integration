# TF5 QLab Integration

A unified Python script for controlling TF5 sound consoles from QLab 5 using OSC commands.

## Features

- **Scene Recall**: Recall TF5 scenes with simple scene IDs (A01, B20, etc.)
- **Channel Control**: Control multiple channels with on/off, mute, level, and pan
- **OSC Commands**: Uses the only command format that works with TF5 consoles
- **No Quotes Needed**: Clean command syntax without complex quoting
- **Multi-line Support**: Readable multi-line commands in QLab

## Quick Start

### Scene Recall
```bash
python TF5_QLab_Control.py scene B02
```

### Channel Control
```bash
python TF5_QLab_Control.py channel 1:on,2:off,3:level:0
```

## QLab Integration

### Scene Recall
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py scene B02"
end tell
```

### Channel Control
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel 1:on,2:off,3:level:0"
end tell
```

## Command Reference

| Command Type | Usage | Example |
|--------------|-------|---------|
| Scene Recall | `scene <scene_id>` | `scene B02` |
| Channel Control | `channel <commands>` | `channel 1:on,2:off,3:level:0` |

### Channel Commands
- `channel:on/off` - basic control
- `channel:mute/unmute` - mute control  
- `channel:level:-100 to +10` - volume (direct dB values)
- `channel:pan:-1.0 to 1.0` - pan control

## Requirements

- Python 3
- TF5 console on IP `192.168.0.95` port `49280`
- QLab 5
- Network connectivity between QLab and TF5

## Files

- `TF5_QLab_Control.py` - Main unified control script
- `TF5_QLab_Instructions.md` - Detailed setup and usage instructions
- `MultiCh.py` - Original reference script using OSC commands

## License

MIT License - see LICENSE file for details.
