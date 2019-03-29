from .settings import *

DEBUG = False

# Done a la pedreiro just to get it work. Should really read the docs better and tweak configs
# in order to NOT need this function
def _show_toolbar(request):
    return False


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": _show_toolbar,
}

ALLOWED_HOSTS = ['*']
