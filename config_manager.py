import configparser

# Load configuration from file
def load_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

# Save runner names to config file
def save_runners_to_config(runner_names, file_path='config.ini'):
    config = load_config(file_path)
    config['settings']['runners'] = ','.join([f'"{name}"' for name in runner_names])
    with open(file_path, 'w') as configfile:
        config.write(configfile)
    print(f"Runners saved to {file_path}")
