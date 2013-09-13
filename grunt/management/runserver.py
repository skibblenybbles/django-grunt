from django.contrib.staticfiles.management.commands.runserver import \
    Command as RunserverCommandBase
from django.core import management
from django.core.management.base import BaseCommand

from .standard import StandardCommand


class RunserverCommandMixin(object):
    """
    Runserver management command options.
    
    """
    option_list = RunserverCommandBase.option_list[len(BaseCommand.option_list):]
    option_groups = (
        ("[runserver options]",
            "These options will be passed to runserver.",
            option_list,
        ),)
    option_names = ()
    actions = ("runserver",)
    
    def handle_runserver(self):
        if self.options["verbosity"] >= 1:
            self.stdout.write(
                "\n    > runserver\n\n")
        management.call_command("runserver", *self.args, **self.options)


class RunserverCommand(RunserverCommandMixin, StandardCommand):
    """
    Runserver management command.
    
    """
    option_list = \
        StandardCommand.option_list
    option_groups = \
        RunserverCommandMixin.option_groups + \
        StandardCommand.option_groups
    option_names = \
        RunserverCommandMixin.option_names + \
        StandardCommand.option_names
    actions = \
        RunserverCommandMixin.actions + \
        StandardCommand.actions
