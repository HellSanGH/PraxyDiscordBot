def load_properties(filepath):
    properties = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                if value.startswith('0x'):
                    try:
                        properties[key] = int(value, 16)
                    except ValueError:
                        properties[key] = value
                elif value.lower() == 'true':
                    properties[key] = True
                elif value.lower() == 'false':
                    properties[key] = False
                else:
                    properties[key] = value
    return properties


config = {}

def init_config(properties_file='bot.properties'):
    global config
    config.update(load_properties(properties_file))

