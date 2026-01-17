from .models import AppConfig


def app_config(request):
    """
    Context processor to make AppConfig available in all templates.
    Returns the singleton AppConfig instance or None if it doesn't exist.
    """
    try:
        app_config = AppConfig.load()
        if app_config.is_active:
            return {'app_config': app_config}
    except Exception:
        pass
    return {'app_config': None}

