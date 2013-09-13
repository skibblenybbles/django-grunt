from django.conf import settings

from ..conf import grunt_conf


class GruntConfigMixin(object):
    """
    A view mixin for updating a context dictionary with grunt
    configuration data.
    
    """
    grunt_config_key = None
    
    def grunt_config(self, config=None, key=None):
        return grunt_conf(
            config={} if config is None else config,
            key=key if key is None else self.grunt_config_key)
