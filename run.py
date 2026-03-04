import os
import yaml
import time
import subprocess
import sys

def parse_env_to_dict():
    """
    Parses environment variables prefixed with ART_ into a nested dictionary.
    Keys are split by __ to create nested structures. 
    E.g. ART_QBITTORRENT__HOST=127.0.0.1 -> {'qbittorrent': {'host': '127.0.0.1'}}
    """
    from typing import Dict, Any
    config: Dict[str, Any] = {}
    for key, value in os.environ.items():
        if key.startswith("ART_") and len(key) > 4:
            path = key[4:]
            parts = path.split("__")
            
            current: Any = config
            for i, part in enumerate(parts):
                # use lower case key names as autoremove-torrents expects lowercase config keys
                part_lower = part.lower() 
                if i == len(parts) - 1:
                    # try to parse booleans and numbers
                    val_lower = value.lower()
                    if val_lower == 'true':
                        current[part_lower] = True
                    elif val_lower == 'false':
                        current[part_lower] = False
                    else:
                        try:
                            if '.' in value:
                                current[part_lower] = float(value)
                            else:
                                current[part_lower] = int(value)
                        except ValueError:
                            current[part_lower] = value
                else:
                    if part_lower not in current:
                        current[part_lower] = {}
                    current = current[part_lower]
    return config

def merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1. dict2 values overwrite dict1 values.
    """
    for k, v in dict2.items():
        if isinstance(v, dict) and k in dict1 and isinstance(dict1[k], dict):
            merge_dicts(dict1[k], v)
        else:
            dict1[k] = v
    return dict1

def main():
    config_path = "/config/config.yml"
    temp_config_path = "/tmp/config.yml"
    
    # get the integer interval or default to 3600 (1 hour)
    try:
        interval = int(os.environ.get("INTERVAL", "3600"))
    except ValueError:
        print("Invalid INTERVAL specified. Defaulting to 3600.", file=sys.stderr)
        interval = 3600
        
    print(f"Starting wrapper. Interval set to {interval} seconds.", flush=True)

    while True:
        base_config = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    content = yaml.safe_load(f)
                    if content and isinstance(content, dict):
                        base_config = content
                    else:
                        print(f"Warning: Base config at {config_path} is empty or not a valid dictionary.", file=sys.stderr)
            except yaml.YAMLError as exc:
                print(f"Error parsing {config_path}: {exc}", file=sys.stderr)
            except IOError as exc:
                print(f"Error reading {config_path}: {exc}", file=sys.stderr)
        
        env_config = parse_env_to_dict()
        merged_config = merge_dicts(base_config, env_config)
        
        try:
            with open(temp_config_path, "w", encoding="utf-8") as f:
                yaml.dump(merged_config, f, default_flow_style=False)
        except IOError as exc:
            print(f"Failed to write temp config file {temp_config_path}: {exc}", file=sys.stderr)
        else:
            print("Running autoremove-torrents...", flush=True)
            try:
                subprocess.run(
                    ["autoremove-torrents", "-c", temp_config_path],
                    cwd="/tmp",
                    check=False
                )
            except FileNotFoundError:
                print("Error: autoremove-torrents executable not found.", file=sys.stderr)
            except Exception as e:
                print(f"Error running autoremove-torrents: {e}", file=sys.stderr)
            print("autoremove-torrents execution finished.", flush=True)

        print(f"Sleeping for {interval} seconds...", flush=True)
        time.sleep(interval)

if __name__ == "__main__":
    main()
