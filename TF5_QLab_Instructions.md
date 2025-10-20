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
python TF5_QLab_Control.py channels <groups>
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

## Individual Channel Control

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

## Group Channel Control (NEW)

### **Command:**
```bash
python TF5_QLab_Control.py channels on:1,2,3,4 off:5,6,7
```

### **QLab AppleScript:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
	do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels on:1,2,3,4 off:5,6,7"
end tell
```

### **Multi-line Commands:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
	do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels " & ¬
		"on:1,2,3,4,5,6,7,8,9,10," & ¬
		"off:11,12,13,14,15,16,17,18," & ¬
		"mute:19,20,21,22,23,24"
end tell
```

### **Command Formats:**
- `on:1,2,3,4` - turn on multiple channels
- `off:5,6,7` - turn off multiple channels
- `mute:8,9,10` - mute multiple channels
- `unmute:11,12,13` - unmute multiple channels

### **Examples:**
- `on:1,2,3,4 off:5,6,7` → turn on ch1-4, turn off ch5-7
- `mute:8,9,10 on:1,2,3` → mute ch8-10, turn on ch1-3
- `off:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18` → turn off all channels 1-18

---

## Complete QLab AppleScript Examples

### **Scene Recall Examples**

**Basic Scene Recall:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py scene B02"
end tell
```

**Scene with Double Digits:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py scene A15"
end tell
```

**Scene with Space (Quoted):**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py scene \"A 03\""
end tell
```

### **Individual Channel Control Examples**

**Basic On/Off and Level Control:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel 1:on,2:off,3:level:0"
end tell
```

**Level, Mute, and Pan Control:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel 1:level:0.8,2:mute,3:pan:0.5"
end tell
```

**Complex Multi-Channel Control:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel 1:on,2:level:-10,3:off,4:level:5,5:pan:-0.5"
end tell
```

**All Channels 1-18 to Level 0:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel 1:level:0,2:level:0,3:level:0,4:level:0,5:level:0,6:level:0,7:level:0,8:level:0,9:level:0,10:level:0,11:level:0,12:level:0,13:level:0,14:level:0,15:level:0,16:level:0,17:level:0,18:level:0"
end tell
```

### **Group Channel Control Examples (NEW)**

**Turn On Channels 1-4, Turn Off 5-7:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels on:1,2,3,4 off:5,6,7"
end tell
```

**Mute Channels 8-10, Turn On 1-3:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels mute:8,9,10 on:1,2,3"
end tell
```

**Turn Off All Channels 1-18:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels off:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

**Turn On All Channels 1-18:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels on:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

**Mute All Channels 1-18:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels mute:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

**Unmute All Channels 1-18:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels unmute:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

### **Multi-line Scripts for Readability**

**Complex Channel Control (Multi-line):**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel " & ¬
        "1:on,2:off,3:level:0," & ¬
        "4:mute,5:pan:0.5,6:level:-10," & ¬
        "7:unmute,8:level:5,9:pan:-0.5"
end tell
```

**Complex Group Control (Multi-line):**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels " & ¬
        "on:1,2,3,4,5,6,7,8,9,10," & ¬
        "off:11,12,13,14,15,16,17,18," & ¬
        "mute:19,20,21,22,23,24"
end tell
```

### **Common Show Scenarios**

**Scene Change:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py scene B02"
end tell
```

**Mic Check - All On:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels on:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

**Mic Check - All Off:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels off:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

**Band Setup (Turn on band mics, turn off vocal mics):**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels on:1,2,3,4,5,6 off:7,8,9,10,11,12"
end tell
```

**Vocal Setup (Turn off band mics, turn on vocal mics):**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels off:1,2,3,4,5,6 on:7,8,9,10,11,12"
end tell
```

**Mute All:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels mute:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

**Unmute All:**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channels unmute:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"
end tell
```

**Level Reset (Reset all levels to 0dB):**
```applescript
tell application id "com.figure53.QLab.5" to tell front workspace
    do shell script "python3 ~/Desktop/TFxQLab/TF5_QLab_Control.py channel 1:level:0,2:level:0,3:level:0,4:level:0,5:level:0,6:level:0,7:level:0,8:level:0,9:level:0,10:level:0,11:level:0,12:level:0,13:level:0,14:level:0,15:level:0,16:level:0,17:level:0,18:level:0"
end tell
```

---

## Quick Reference

| Command Type | Usage | Example |
|--------------|-------|---------|
| Scene Recall | `scene <scene_id>` | `scene B02` |
| Individual Channel Control | `channel <commands>` | `channel 1:on,2:off,3:level:0` |
| Group Channel Control | `channels <groups>` | `channels on:1,2,3,4 off:5,6,7` |

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
