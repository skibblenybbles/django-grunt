import optparse
import os
import subprocess

from django.core.management.base import CommandError

from .collectstatic import CollectstaticCommand


class GruntCommandMixin(object):
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
    
    def validate_grunt(self):
        # Is grunt available?
        with open(os.devnull, "w") as null:
            try:
                subprocess.check_call(("which", "grunt",),
                    stdout=null, stderr=null)
            except subprocess.CalledProcessError:
                raise CommandError(
                    "grunt is not available on the command line. Please ensure "
                    "that grunt is installed and reachable in your $PATH.")
    
    def handle_grunt(self):
        if self.options["verbosity"] >= 1:
            self.stdout.write(
                "\n    > grunt {args:s}\n\n".format(
                    args=" ".join(self.args)))
        
        with open(os.devnull, "w") as null:
            try:
                subprocess.check_call(
                    ("grunt",) + \
                        self.args + \
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
                            else ()),
                    stdout=self.stdout if self.options["verbosity"] >= 1 else null,
                    stderr=self.stderr if self.options["verbosity"] >= 1 else null)
            except subprocess.CalledProcessError, e:
                raise CommandError(
                    "grunt failed with exit code {code:d}.".format(
                        code=e.returncode))


class GruntCommand(GruntCommandMixin, CollectstaticCommand):
    option_list = \
        CollectstaticCommand.option_list
    option_groups = \
        GruntCommandMixin.option_groups + \
        CollectstaticCommand.option_groups
    option_names = \
        GruntCommandMixin.option_names + \
        CollectstaticCommand.option_names
    actions = \
        CollectstaticCommand.actions + \
        GruntCommandMixin.actions
    args = "[grunt command ...] ([grunt option] | [collectstatic option] | [standard option])*"
    help = "Collect static files in a single location and run grunt."
