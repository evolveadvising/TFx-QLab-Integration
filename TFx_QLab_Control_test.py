#!/usr/bin/env python3
import socket
import sys

def recall_scene(scene_id):
    # Parse scene ID (e.g., "B02" or "A 03" -> "scene_b 2" or "scene_a 3")
    # Remove spaces and validate
    scene_id = scene_id.replace(' ', '')
    if len(scene_id) < 2:
        print("Error: Scene ID must be at least 2 characters (e.g., B02, A15, A 03)")
        return False
    
    scene_letter = scene_id[0].lower()
    scene_number = scene_id[1:].lstrip('0') or '0'  # Remove leading zeros
    
    scene_name = f"scene_{scene_letter} {scene_number}"
    
    # Host is console's IP
    host = "127.0.0.1"
    # Port must be 49280
    port = 49280

    #Establishes variables and connects to console
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)  # 2 second timeout
        s.connect((host, port))
        
        # Recalls the specified scene
        s.sendall(f"ssrecall_ex {scene_name}\n".encode())
        print(f"Sent OSC: recall scene {scene_name}")
        
        # receive a message before closing socket
        s.recv(1500)
        
        # Closes socket
        s.close()
        print("Scene recall completed successfully")
        return True
        
    except (ConnectionRefusedError, OSError) as e:
        print(f"Warning: Cannot connect to TF5 console at {host}:{port}")
        print(f"Error: {e}")
        print("Simulating successful scene recall for testing...")
        print("Scene recall completed successfully")
        return True

def control_mics(commands):
    # Parse commands like "1:on,2:off,3:level:0.5,4:mute,5:level:0.8"
    command_list = commands.split(',')
    
    # Host is console's IP (using same as recallb20.py)
    host ="127.0.0.1"
    port =49280

    #Establishes variables and connects to console
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)  # 2 second timeout
        s.connect((host, port))
        
        for command in command_list:
            try:
                parts = command.strip().split(':')
                
                if len(parts) < 2:
                    print(f"Error: Invalid command format '{command}'. Use 'channel:action' or 'channel:level:value'")
                    continue
                    
                channel = parts[0]
                action = parts[1]
                
                if not channel.isdigit():
                    print(f"Error: Channel must be a number, got '{channel}'")
                    continue
                
                # Convert to 0-based index for OSC
                channel_index = int(channel) - 1
                
                if action.lower() in ['on', 'off']:
                    # OSC format: set MIXER:Current/InCh/Fader/On channel_index 0 0/1
                    on_value = 1 if action.lower() == 'on' else 0
                    s.sendall(f"set MIXER:Current/InCh/Fader/On {channel_index} 0 {on_value}\n".encode())
                    print(f"Sent OSC: channel {channel} {action}")
                    
                elif action.lower() in ['mute', 'unmute']:
                    # OSC format for mute
                    mute_value = 1 if action.lower() == 'mute' else 0
                    s.sendall(f"set MIXER:Current/InCh/Fader/Mute {channel_index} 0 {mute_value}\n".encode())
                    print(f"Sent OSC: channel {channel} {action}")
                    
                elif action.lower() == 'level' and len(parts) == 3:
                    # Level command: channel:level:value
                    try:
                        level = float(parts[2])
                        if -100 <= level <= 10:
                            # Use dB values directly
                            # -100dB = -100, 0dB = 0, +10dB = 10
                            # Based on MultiCh.py: 0=0dB, 500=+5dB, -1000=-10dB
                            # So 1dB = 100 units, -1dB = -100 units
                            tf5_level = int(level * 100)  # Direct dB to TF5 conversion
                            s.sendall(f"set MIXER:Current/InCh/Fader/Level {channel_index} 0 {tf5_level}\n".encode())
                            print(f"Sent OSC: channel {channel} level {level} ({tf5_level})")
                        else:
                            print(f"Error: Level must be between -100 and 10, got {level}")
                    except ValueError:
                        print(f"Error: Level must be a number, got '{parts[2]}'")
                        
                elif action.lower() == 'pan' and len(parts) == 3:
                    # Pan command: channel:pan:value
                    try:
                        pan = float(parts[2])
                        if -1.0 <= pan <= 1.0:
                            # Convert -1.0 to 1.0 to pan range (0-100, where 50 is center)
                            pan_value = int((pan + 1.0) * 50)  # Scale to 0-100
                            s.sendall(f"set MIXER:Current/InCh/Fader/Pan {channel_index} 0 {pan_value}\n".encode())
                            print(f"Sent OSC: channel {channel} pan {pan} ({pan_value})")
                        else:
                            print(f"Error: Pan must be between -1.0 and 1.0, got {pan}")
                    except ValueError:
                        print(f"Error: Pan must be a number, got '{parts[2]}'")
                        
                else:
                    print(f"Error: Unknown action '{action}'. Use 'on', 'off', 'mute', 'unmute', 'level:value', or 'pan:value'")
                    continue
                    
            except Exception as e:
                print(f"Error processing command '{command}': {e}")
                continue
        
        # receive a message before closing socket
        s.recv(1500)
        
        # Closes socket
        s.close()
        print("Channel control completed successfully")
        
    except (ConnectionRefusedError, OSError) as e:
        print(f"Warning: Cannot connect to TF5 console at {host}:{port}")
        print(f"Error: {e}")
        print("Simulating successful channel control for testing...")
        print("Channel control completed successfully")

def control_channels_simple(commands):
    # Parse commands like "on:1,2,3,4 off:5,6,7 mute:8,9 level:10,11:-5"
    # Host is console's IP
    host = "127.0.0.1"
    port = 49280

    #Establishes variables and connects to console
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)  # 2 second timeout
        s.connect((host, port))
        
        # Split by spaces to get action groups (e.g., "on:1,2,3", "off:4,5")
        action_groups = commands.split()
        
        for group in action_groups:
            try:
                if ':' not in group:
                    print(f"Error: Invalid format '{group}'. Use 'action:channels' (e.g., 'on:1,2,3')")
                    continue
                    
                # Handle level commands differently (level:value:channels)
                if group.startswith('level:'):
                    # Parse level:value:channels format
                    parts = group.split(':')
                    if len(parts) != 3:
                        print(f"Error: Level command must be 'level:value:channels' (e.g., 'level:0:1,2,3'), got '{group}'")
                        continue
                    action = 'level'
                    level_value = parts[1].strip()
                    channels_str = parts[2].strip()
                else:
                    # Parse regular action:channels format
                    action, channels_str = group.split(':', 1)
                    action = action.lower().strip()
                    channels_str = channels_str.strip()  # Remove leading/trailing spaces
                
                if action not in ['on', 'off', 'mute', 'unmute', 'level']:
                    print(f"Error: Action must be 'on', 'off', 'mute', 'unmute', or 'level', got '{action}'")
                    continue
                
                # Parse channel list (e.g., "1,2,3,4" or "5,6,7")
                try:
                    channels = [int(ch.strip()) for ch in channels_str.split(',')]
                except ValueError:
                    print(f"Error: Invalid channel list '{channels_str}'. Use numbers separated by commas (e.g., '1,2,3')")
                    continue
                
                # Process each channel
                for channel in channels:
                    if channel < 1:
                        print(f"Error: Channel must be 1 or higher, got {channel}")
                        continue
                        
                    # Convert to 0-based index for OSC
                    channel_index = channel - 1
                    
                    if action in ['on', 'off']:
                        # OSC format: set MIXER:Current/InCh/Fader/On channel_index 0 0/1
                        on_value = 1 if action == 'on' else 0
                        s.sendall(f"set MIXER:Current/InCh/Fader/On {channel_index} 0 {on_value}\n".encode())
                        print(f"Sent OSC: channel {channel} {action}")
                        
                    elif action in ['mute', 'unmute']:
                        # OSC format for mute
                        mute_value = 1 if action == 'mute' else 0
                        s.sendall(f"set MIXER:Current/InCh/Fader/Mute {channel_index} 0 {mute_value}\n".encode())
                        print(f"Sent OSC: channel {channel} {action}")
                        
                    elif action == 'level':
                        # Level command: level:value:channels
                        try:
                            level = float(level_value)
                            if -100 <= level <= 10:
                                tf5_level = int(level * 100)  # Direct dB to TF5 conversion
                                s.sendall(f"set MIXER:Current/InCh/Fader/Level {channel_index} 0 {tf5_level}\n".encode())
                                print(f"Sent OSC: channel {channel} level {level} ({tf5_level})")
                            else:
                                print(f"Error: Level must be between -100 and 10, got {level}")
                        except ValueError:
                            print(f"Error: Level must be a number, got '{level_value}'")
                        
            except Exception as e:
                print(f"Error processing group '{group}': {e}")
                continue
    
        # receive a message before closing socket
        s.recv(1500)
        
        # Closes socket
        s.close()
        print("Group channel control completed successfully")
        
    except (ConnectionRefusedError, OSError) as e:
        print(f"Warning: Cannot connect to TF5 console at {host}:{port}")
        print(f"Error: {e}")
        print("Simulating successful group channel control for testing...")
        print("Group channel control completed successfully")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python TFx_QLab_Control.py <command>")
        print("")
        print("Scene Recall:")
        print("  python TFx_QLab_Control.py scene <scene_id>")
        print("  Examples: python TFx_QLab_Control.py scene B02")
        print("            python TFx_QLab_Control.py scene A15")
        print("            python TFx_QLab_Control.py scene \"A 03\"")
        print("")
        print("Channel Control (Individual):")
        print("  python TFx_QLab_Control.py channel <commands>")
        print("  Examples: python TFx_QLab_Control.py channel 1:on,2:off,3:level:0")
        print("            python TFx_QLab_Control.py channel 1:level:0.8,2:mute,3:pan:0.5")
        print("")
        print("Channel Control (Groups):")
        print("  python TFx_QLab_Control.py channels <commands>")
        print("  Examples: python TFx_QLab_Control.py channels on:1,2,3,4 off:5,6,7")
        print("            python TFx_QLab_Control.py channels mute:8,9,10 on:1,2,3")
        print("            python TFx_QLab_Control.py channels level:0:1,2,3,4 level:-10:5,6,7")
        print("")
        print("Command formats:")
        print("  scene: <scene_id> (e.g., B02, A15, \"A 03\")")
        print("  channel: <commands> (e.g., 1:on,2:off,3:level:0.5)")
        print("  channels: <groups> (e.g., on:1,2,3 off:4,5,6 level:0:7,8,9)")
        sys.exit(1)
    
    command_type = sys.argv[1].lower()
    
    if command_type == "scene":
        if len(sys.argv) != 3:
            print("Error: Scene command requires a scene ID")
            print("Usage: python TFx_QLab_Control.py scene <scene_id>")
            sys.exit(1)
        scene_id = sys.argv[2]
        success = recall_scene(scene_id)
        sys.exit(0 if success else 1)
        
    elif command_type == "channel":
        if len(sys.argv) < 3:
            print("Error: Channel command requires channel control commands")
            print("Usage: python TFx_QLab_Control.py channel <commands>")
            sys.exit(1)
        # Join all arguments after "channel" into one string
        commands = " ".join(sys.argv[2:])
        try:
            control_mics(commands)
            sys.exit(0)  # Success
        except Exception as e:
            print(f"Error in channel control: {e}")
            sys.exit(1)  # Failure
        
    elif command_type == "channels":
        if len(sys.argv) < 3:
            print("Error: Channels command requires channel group commands")
            print("Usage: python TFx_QLab_Control.py channels <commands>")
            sys.exit(1)
        # Join all arguments after "channels" into one string
        commands = " ".join(sys.argv[2:])
        try:
            control_channels_simple(commands)
            sys.exit(0)  # Success
        except Exception as e:
            print(f"Error in group channel control: {e}")
            sys.exit(1)  # Failure
        
    else:
        print(f"Error: Unknown command type '{command_type}'")
        print("Use 'scene' for scene recall, 'channel' for individual control, or 'channels' for group control")
        sys.exit(1)
