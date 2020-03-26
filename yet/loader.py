import yaml

from yet.structures import *


# Handle YAML loading

class YeTLoader(yaml.SafeLoader):
    """
    Customized YAML loader to accommodate YeT style.
    Use 'list of singleton dict-like container'
    instead of returning single dict for everything.
    Advantages: handle duplicate keys, preserve order.
    """
    def __init__(self, stream):
        self.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            self._construct_mapping)
        super(YeTLoader, self).__init__(stream)

    @staticmethod
    def _construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return [Command(k, v) if isinstance(v, str) or k.startswith('_')
                else Environment(k, v)
                for k, v in loader.construct_pairs(node)]


def load_yet(stream):
    return yaml.load(stream, Loader=YeTLoader)
