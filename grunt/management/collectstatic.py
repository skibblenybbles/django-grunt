import optparse

from django.contrib.staticfiles.management.commands.collectstatic import \
    Command as CollectStaticCommandBase
from django.core import management
from django.core.management.base import NoArgsCommand

from .standard import StandardCommand


class CollectstaticCommandMixin(object):
    """
    Collectstatic management command options.
    
    """
    option_list = (
        optparse.make_option("--nocollect",
            action="store_false", dest="collect", default=True,
            help="Do NOT run collectstatic"),
    ) + CollectStaticCommandBase.option_list[len(NoArgsCommand.option_list):]
    option_groups = (
        ("[collectstatic] commands",
            "These options will be passed to collectstatic.",
            option_list,
        ),)
    option_names = ("collect",)
    actions = ("collectstatic",)
    
    def parse_option_collect(self):
        return bool(self.options.get("collect", False))
    
    def handle_collectstatic(self):
        if self.options["collect"]:
            if self.options["verbosity"] >= 1:
                self.stdout.write(
                    "\n    > collectstatic\n")
            management.call_command("collectstatic", **self.options)


class CollectstaticCommand(CollectstaticCommandMixin, StandardCommand):
    """
    Collectstatic management command.
    
    """
    option_list = \
        StandardCommand.option_list
    option_groups = \
        CollectstaticCommandMixin.option_groups + \
        StandardCommand.option_groups
    option_names = \
        CollectstaticCommandMixin.option_names + \
        StandardCommand.option_names
    actions = \
        CollectstaticCommandMixin.actions + \
        StandardCommand.actions
