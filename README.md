# TFx QLab Integration

A Python-based integration system for controlling **Yamaha TFx series sound consoles** from **QLab 5** using OSC commands.
Works with TF3 and TF5 soundboards. Others are untested.

## Overview

This project provides a unified Python script that enables seamless control of Yamaha TFx sound consoles directly from QLab 5 show control software. The system supports scene recall, individual channel control, and group channel operations through simple command-line interfaces that integrate perfectly with QLab's scripting capabilities.

## Features

### 🎭 **Scene Recall**
- Recall TFx console scenes with simple scene IDs (A01, B20, C15, etc.)
- Automatic scene ID parsing and validation
- Support for spaces in scene names (e.g., "A 03" → A3)

### 🎛️ **Individual Channel Control**
- **On/Off Control**: Turn channels on or off
- **Mute/Unmute**: Mute or unmute individual channels
- **Level Control**: Set precise dB levels (-100 to +10 dB)
- **Pan Control**: Adjust stereo panning (-1.0 to 1.0)

### 🎚️ **Group Channel Control**
- **Bulk Operations**: Control multiple channels simultaneously
- **Mixed Commands**: Combine on/off, mute, and level operations
- **Level Groups**: Set specific levels for multiple channels at once
- **Efficient Commands**: Reduce QLab script complexity

### 🔧 **Technical Features**
- **OSC Protocol**: Uses the only command format that works with TFx consoles
- **Error Handling**: Robust connection timeout and error recovery
- **Testing Mode**: Localhost testing without physical console
- **No Quotes Required**: Clean command syntax without complex escaping

## Quick Start

### Scene Recall
```bash
python TFx_QLab_Control.py scene B02
```

### Individual Channel Control
```bash
python TFx_QLab_Control.py channel 1:on,2:off,3:level:0
```

### Group Channel Control
```bash
python TFx_QLab_Control.py channels on:1,2,3,4 off:5,6,7
```

## QLab Integration

### Scene Recall in QLab
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TFx_QLab_Control.py scene B02"
end tell
```

### Channel Control in QLab
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TFx_QLab_Control.py channel 1:on,2:off,3:level:0"
end tell
```

### Group Control in QLab
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TFx_QLab_Control.py channels on:1,2,3,4 off:5,6,7"
end tell
```

## Command Reference

| Command Type | Usage | Example |
|--------------|-------|---------|
| Scene Recall | `scene <scene_id>` | `scene B02` |
| Individual Channel Control | `channel <commands>` | `channel 1:on,2:off,3:level:0` |
| Group Channel Control | `channels <groups>` | `channels on:1,2,3,4 off:5,6,7` |
| Group Level Control | `channels level:value:channels` | `channels level:0:1,2,3,4,5` |

### Channel Commands
- `channel:on/off` - Basic on/off control
- `channel:mute/unmute` - Mute/unmute control  
- `channel:level:-100 to +10` - Volume control (direct dB values)
- `channel:pan:-1.0 to 1.0` - Pan control

### Group Commands
- `on:1,2,3,4` - Turn on multiple channels
- `off:5,6,7` - Turn off multiple channels
- `mute:8,9,10` - Mute multiple channels
- `unmute:11,12,13` - Unmute multiple channels
- `level:0:1,2,3,4` - Set level for multiple channels

## Files Included

### Core Scripts
- **`TFx_QLab_Control.py`** - Main production script (IP: 192.168.0.95)
- **`TFx_QLab_Control_test.py`** - Test script for development (IP: 127.0.0.1)

### Configuration Files
- **`TF_ConsoleFile.tff`** - TFx console configuration file
- **`QLab TF Template.qlab5`** - QLab workspace template with example cues

### Documentation
- **`TFx_QLab_Instructions.html`** - Comprehensive setup and usage guide
- **`README.md`** - This file

### Backup Files
- **`QLab TF Template backups/`** - Versioned backups of QLab workspace

## Requirements

- **Python 3** - Required for script execution
- **QLab 5** - Show control software
- **Yamaha TFx Console** - TF1, TF3, TF5, or other TFx series
- **Network Connectivity** - Between QLab computer and TFx console
- **OSC Support** - TFx console must have OSC enabled

## Network Setup

### TFx Console Configuration
- **IP Address**: Configure TFx console to use `192.168.0.95`
- **Port**: Ensure port `49280` is open for OSC communication
- **OSC**: Enable OSC control in TFx console settings

### Computer Configuration
- **Network**: Ensure computer is on same network as TFx console
- **IP Range**: Use compatible IP range (e.g., 192.168.0.100)
- **Firewall**: Allow Python scripts to access network

## Common Use Cases

### 🎪 **Live Theater**
- Scene changes between acts
- Mic check routines
- Band vs. vocal mic switching
- Emergency mute all

### 🎵 **Concerts & Events**
- Sound check automation
- Performance scene recall
- Monitor mix adjustments
- FOH control integration

### 🎬 **Broadcast & Recording**
- Automated scene switching
- Channel level management
- Mute group operations
- Real-time adjustments

## Examples

### Sound Check Setup
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TFx_QLab_Control.py channels " & ¬
        "on:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18 " & ¬
        "level:0:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

### Band Setup (Turn on band mics, turn off vocal mics)
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TFx_QLab_Control.py channels on:1,2,3,4,5,6 off:7,8,9,10,11,12"
end tell
```

### Emergency Mute All
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TFx_QLab_Control.py channels mute:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

## Troubleshooting

### Common Issues
1. **"Can't make script" error** - Use absolute file paths in QLab
2. **Nothing happens** - Check TFx IP address and network connection
3. **Script not found** - Verify file paths in QLab scripts
4. **Permission denied** - Ensure Python 3 is installed and accessible

### Testing
```bash
# Test from terminal
cd /Users/alanleard/Desktop/TFxQLab
python3 TFx_QLab_Control.py scene B02
python3 TFx_QLab_Control.py channel 1:on,2:off,3:level:0
```

## OSC Commands Used

- `ssrecall_ex scene_X Y` - Scene recall
- `set MIXER:Current/InCh/Fader/On {channel} 0 {0|1}` - On/Off
- `set MIXER:Current/InCh/Fader/Level {channel} 0 {dB_value * 100}` - Level
- `set MIXER:Current/InCh/Fader/Mute {channel} 0 {0|1}` - Mute
- `set MIXER:Current/InCh/Fader/Pan {channel} 0 {pan_value}` - Pan

## License

MIT License - see LICENSE file for details.

## Support

For detailed setup instructions, examples, and troubleshooting, see `TFx_QLab_Instructions.html`.

---

**Note**: This integration is specifically designed for Yamaha TFx series consoles and requires QLab 5. Always test before using in live shows.
