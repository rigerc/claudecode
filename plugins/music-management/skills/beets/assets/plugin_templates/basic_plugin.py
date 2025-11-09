"""
Basic Beets Plugin Template

A minimal plugin template that demonstrates the basic structure of a beets plugin.
Copy this file to ~/.config/beets/plugins/your_plugin_name/your_plugin_name.py
and customize as needed.
"""

from beets import config
from beets.plugins import BeetsPlugin


class YourPluginName(BeetsPlugin):
    """
    Replace this with a description of what your plugin does.
    """

    def __init__(self):
        super().__init__()

        # Add default configuration options
        self.config.add({
            'enabled': True,
            'option1': 'default_value',
            'option2': 123
        })

        # Register template functions (optional)
        # self.template_funcs["your_plugin_func"] = self._template_function

        # Register event listeners (optional)
        # self.register_listener('item_imported', self.item_imported)

    def _template_function(self, text):
        """Example template function."""
        if not text:
            return ""
        return text.upper()  # Example transformation

    def item_imported(self, lib, item):
        """Called when an item is imported."""
        if self.config['enabled'].get(bool):
            self._log.info(f'Processing imported item: {item.artist} - {item.title}')
            # Add your import processing logic here

    # Example command registration
    """
    def commands(self):
        """Register custom commands."""
        cmd = Subcommand('yourcommand', help='Your custom command')
        cmd.parser.add_option('-d', '--debug', action='store_true')
        cmd.func = self._your_command
        return [cmd]

    def _your_command(self, lib, opts, args):
        '''Custom command implementation.'''
        self._log.info('Running your command')
        if opts.debug:
            self._log.debug('Debug mode enabled')

        # Your command logic here
        for item in lib.items(args):
            print(f'{item.artist} - {item.title}')
    """