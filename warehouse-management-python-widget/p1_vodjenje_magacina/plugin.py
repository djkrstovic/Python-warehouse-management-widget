from plugin_framework.plugin import Plugin
from .widgets.magacin_widget import MagacinWidget

class Main(Plugin):
    def __init__(self, spec):
        super().__init__(spec)

    def get_widget(self, parent=None):
        return MagacinWidget(parent), None, None
