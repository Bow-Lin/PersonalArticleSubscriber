from pathlib import Path

def load_config(config_path="config.yaml"):
    """Load configuration from a YAML or JSON file"""
    config_path = Path(config_path)
    if config_path.suffix in ('.yaml', '.yml'):
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif config_path.suffix == '.json':
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise ValueError("Config file must be either YAML or JSON format") 