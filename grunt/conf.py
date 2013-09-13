from django.conf import settings


def grunt_conf(config=None, key=None):
    """
    Returns the grunt configuration settings. Optionally updates
    the dictionary passed to config. In the output dictionary,
    optionally nests the grunt configuration settings under
    the given key.
    
    """
    if config is None:
        config = {}
    
    if key is not None:
        if key not in config:
            config[key] = {}
        config = config[key]
    
    config.update({
        "grunt_js": getattr(settings, "GRUNT_JS", False),
        "grunt_css": getattr(settings, "GRUNT_CSS", False),
    })
    
    return config
