import importlib


class PluginConfig(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class AbstractPlugin(object):
    def __init__(self, plugin_config):
        """ Initialize plugin with the passed in configuration
        :param plugin_config: The configuration object required for plugin to work
        :type plugin_config: PluginConfig 
        """
        self.config = plugin_config


class PluginBuilder(object):
    @classmethod
    def build_plugin(cls, class_name, config):
        """Create an instance of the named plugin and return it
        :param class_name: fully qualified name of class 
        :type class_name: str
        :param config: the supporting configuration for plugin 
        :type config: PluginConfig
        :rtype: AbstractPlugin
        :return: an instance of a concrete implementation of AbstractPlugin
        """
        mod_path, class_name = class_name.rsplit('.', 1)
        plugin_cls = getattr(importlib.import_module(mod_path), class_name)
        return plugin_cls(config)

    @classmethod
    def build_plugins(cls, plugins_conf):
        """Create an instance of the named plugin and return it
        :param plugins_conf: dict of {alias: dict(plugin builder params) } 
        :type plugins_conf: dict
        :rtype: dict[str, AbstractPlugin]
        :return: dict of alias: plugin instance
        """
        plugins = {}
        for alias, params_dict in plugins_conf.items():
            plugin_config = PluginConfig(**(params_dict.get('config') or {}))
            plugins[alias] = cls.build_plugin(class_name=params_dict['class_name'], config=plugin_config)
        return plugins
