# TF5 QLab Integration Instructions

## Overview
This document provides instructions for using the unified Python script to control a TF5 sound console from QLab 5. The script uses IP address `192.168.0.95` and port `49280` with OSC command format.

## Main Script

### **TF5_QLab_Control.py** - Unified Control Script
**Purpose**: Single script for both scene recall and channel control

**Usage:**
```bash
python TF5_QLab_Control.py scene <scene_id>
python TF5_QLab_Control.py channel <commands>
```

---

## Scene Recall

### **Command:**
```bash
python TF5_QLab_Control.py scene B02
```

### **QLab AppleScript:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
	do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py scene B02"
end tell
```

### **Examples:**
- `B02` → recalls scene B2
- `A15` → recalls scene A15
- `"A 03"` → recalls scene A3 (with space)

### **Scene ID Format:**
- Use letter (A, B, C) followed by number (01-99)
- Leading zeros are automatically removed (A03 becomes A3)
- Spaces are handled (A 15 becomes A15)

---

## Channel Control

### **Command:**
```bash
python TF5_QLab_Control.py channel 1:on,2:off,3:level:0
```

### **QLab AppleScript:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
	do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel 1:on,2:off,3:level:0"
end tell
```

### **Multi-line Commands:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
	do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel " & ¬
		"1:on,2:off,3:level:0," & ¬
		"4:mute,5:pan:0.5,6:level:-10"
end tell
```

### **Command Formats:**
- `channel:on/off` - basic control
- `channel:mute/unmute` - mute control  
- `channel:level:-100 to +10` - volume (direct dB values)
- `channel:pan:-1.0 to 1.0` - pan control

### **Examples:**
- `1:on,2:off,3:level:0` → turn on ch1, off ch2, set ch3 to 0dB
- `1:level:-5,2:mute,3:pan:0.5` → set ch1 to -5dB, mute ch2, pan ch3 right
- `1:on,2:level:-10,3:off,4:level:5,5:pan:-0.5` → complex multi-channel control

---

## Quick Reference

| Command Type | Usage | Example |
|--------------|-------|---------|
| Scene Recall | `scene <scene_id>` | `scene B02` |
| Channel Control | `channel <commands>` | `channel 1:on,2:off,3:level:0` |

## Setup Instructions

### 1. **File Location**
Place the script in the same directory as your QLab file:
```
/Users/alanleard/Desktop/TFxQLab/
├── TF5_QLab_Control.py
└── YourShow.qlab5
```

### 2. **QLab Setup**
1. Open QLab 5
2. Create a new "Run Script" cue
3. Set the script type to "AppleScript"
4. Copy the appropriate AppleScript code from above
5. Modify the parameters as needed
6. Click "Compile Script" to verify syntax

### 3. **Network Requirements**
- TF5 console must be on IP `192.168.0.95`
- Port `49280` must be open
- Computer running QLab must be on the same network

## Testing

### Test from Terminal:
```bash
cd /Users/alanleard/Desktop/TFxQLab
python3 TF5_QLab_Control.py scene B02
python3 TF5_QLab_Control.py channel 1:on,2:off,3:level:0
```

## Troubleshooting

### Common Issues:
1. **"Can't make script" error**: Use absolute file paths
2. **Nothing happens**: Check TF5 IP address and network connection
3. **Script not found**: Verify file paths in AppleScript
4. **Permission denied**: Ensure Python 3 is installed and accessible

### OSC Commands Used:
- `ssrecall_ex scene_X Y` - Scene recall
- `set MIXER:Current/InCh/Fader/On {channel} 0 {0|1}` - On/Off
- `set MIXER:Current/InCh/Fader/Level {channel} 0 {dB_value * 100}` - Level
- `set MIXER:Current/InCh/Fader/Mute {channel} 0 {0|1}` - Mute
- `set MIXER:Current/InCh/Fader/Pan {channel} 0 {pan_value}` - Pan

## Notes
- Single unified script for all TF5 control
- Uses OSC command format (only format that works with this TF5)
- Channel numbers automatically converted from 1-based to 0-based
- No quotes needed for channel commands
- Always test before using in live shows
