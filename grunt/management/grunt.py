import optparse

from django.core.management import CommandError

from commando import management
from commando.django.contrib.staticfiles.management.collectstatic import CollectStaticCommand


class GruntCommandOptions(management.CommandOptions):
    """
    Grunt management command options.
    
    """
    option_list = (
        optparse.make_option("--grunt-base",
            action="store", type="string", dest="grunt_base", default="",
            help="Specify an alternate base path for Grunt. By default, all "
                "file paths are relative to the Gruntfile."),
        optparse.make_option("--gruntfile",
            action="store", type="string", dest="gruntfile", default="",
            help="Specify an alternate Gruntfile. By default, grunt looks "
                "in the current or parent directories for the nearest "
                "Gruntfile.js or Gruntfile.coffee file."),
        optparse.make_option("--grunt-debug",
            action="store_true", dest="grunt_debug", default=False,
            help="Enable debugging mode for grunt tasks that support it."),)
    option_groups = (
        ("[grunt commands]",
            "These options will be passed on to grunt.",
            option_list),)
    option_names = ("grunt_base", "gruntfile",)
    actions = ("grunt",)
    
    def parse_option_grunt_base(self):
        return self.options.get("grunt_base", "")
    
    def parse_option_gruntfile(self):
        return self.options.get("gruntfile", "")
    
    def parse_option_grunt_debug(self):
        return bool(self.options.get("grunt_debug", False))
    
    def validate_grunt(self, *arguments, **options):
        self.check_program("grunt")
    
    def handle_grunt(self, *arguments, **options):
        return self.call_program("grunt",
            *(tuple(arguments) + \
                (("--base", self.options["grunt_base"]) \
                    if self.options["grunt_base"] \
                    else ()) + \
                (("--gruntfile", self.options["gruntfile"]) \
                    if self.options["gruntfile"] \
                    else ()) + \
                (("--debug",) \
                    if self.options["grunt_debug"] \
                    else ()) + \
                (("--verbose",) \
                    if self.options["verbosity"] >= 3 \
                    else ())))


class GruntCommand(GruntCommandOptions, CollectStaticCommand):
    option_list = \
        CollectStaticCommand.option_list
    option_groups = \
        GruntCommandOptions.option_groups + \
        CollectStaticCommand.option_groups
    actions = \
        CollectStaticCommand.actions + \
        GruntCommandOptions.actions
    args = "[grunt command ...] ([grunt option] | [collectstatic option] | [standard option])*"
    help = "Collect static files in a single location and run grunt."
