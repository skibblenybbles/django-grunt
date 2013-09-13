import optparse

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.importlib import import_module

from .runserver import RunserverCommand


class GruntserverCommandMixin(object):
    """
    Gruntserver management command options.
    
    """
    option_list = (
        optparse.make_option("--no-grunt-js",
            action="store_false", dest="use_build_js", default=True,
            help="Set settings.GRUNT_JS to False",
        ),
        optparse.make_option("--no-grunt-css",
            action="store_false", dest="use_build_css", default=True,
            help="Set settings.GRUNT_CSS to False"),
        optparse.make_option("--no-gzip",
            action="store_false", dest="use_gzip", default=True,
            help="Do NOT add gzip middleware"),)
    option_groups = (
        ("[buildserver options]",
            "These options configure settings and urls for runserver.",
            option_list),)
    option_names = ("use_build_js", "use_build_css", "use_gzip",)
    actions = ("buildserver",)
    
    def parse_option_use_build_js(self):
        return bool(self.options.get("use_build_js", True))
    
    def parse_option_use_build_css(self):
        return bool(self.options.get("use_build_css", True))
    
    def parse_option_use_gzip(self):
        return bool(self.options.get("use_gzip", True))
    
    def handle_buildserver(self):
        # Set up the staticfiles app to serve files in STATIC_ROOT.
        settings.STATICFILES_FINDERS = (
            "django.contrib.staticfiles.finders.FileSystemFinder",
        )
        settings.STATICFILES_DIRS = (
            settings.STATIC_ROOT,
        )
        settings.STATIC_ROOT = ""
        
        # Add staticfiles handler to urls?
        if self.options["use_gzip"]:
            urlconf = import_module(settings.ROOT_URLCONF)
            urlconf.urlpatterns = staticfiles_urlpatterns() + urlconf.urlpatterns
        
        # Use gzip middleware to compress staticfiles?
        if self.options["use_gzip"]:
            if "django.middleware.gzip.GZipMiddleware" not in settings.MIDDLEWARE_CLASSES:
                settings.MIDDLEWARE_CLASSES = (
                    "django.middleware.gzip.GZipMiddleware",
                ) + settings.MIDDLEWARE_CLASSES
        
        # Force runserver to run with the "--nostatic" option so that the
        # middleware gets run for staticfiles requests?
        if self.options["use_gzip"]:
            self.options["use_static_handler"] = False
        
        # Use compiled JavaScript and CSS in the templates?
        settings.GRUNT_JS = self.options["use_build_js"]
        settings.GRUNT_CSS = self.options["use_build_css"]


class GruntserverCommand(GruntserverCommandMixin, RunserverCommand):
    """
    Command that runs the staticfiles runserver command with the
    built static files in settings.STATIC_ROOT and sets
    the values of settings.GRUNT_JS and settings.GRUNT_CSS.
    
    """
    option_list = \
        RunserverCommand.option_list
    option_groups = \
        GruntserverCommandMixin.option_groups + \
        RunserverCommand.option_groups
    option_names = \
        GruntserverCommandMixin.option_names + \
        RunserverCommand.option_names
    actions = \
        GruntserverCommandMixin.actions + \
        RunserverCommand.actions
    args = "[runserver argument ...] ([buildserver option] | [runserver option] | [standard option])*"
    help = \
        "Starts a lightweight Web server for development and also serves "
        "the built static files in STATIC_ROOT."
