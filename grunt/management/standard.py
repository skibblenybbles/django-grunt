import optparse

from .base import Command, BaseCommand
from .quiet import QuietCommand


class StandardCommand(BaseCommand, QuietCommand, Command):
    """
    Base class for enhanced, standard commands.
    
    """
    option_list = QuietCommand.option_list
    option_groups = BaseCommand.option_groups
    option_names = BaseCommand.option_names + QuietCommand.option_names
    actions = ()
