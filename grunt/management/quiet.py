import optparse

from .base import Command


class QuietCommandMixin(object):
    """
    Quiet Django management command options.
    
    """
    option_list = (
        optparse.make_option("-q", "--quiet",
            action="store_true", dest="quiet", default=False,
            help="Do NOT prompt or output anything."),)
    option_groups = ()
    option_names = ("quiet",)
    quiet_names = (
        ("interactive", False),
        ("verbosity", 0),)
    actions = ()
    
    def parse_option_quiet(self):
        quiet = bool(self.options.get("quiet", False))
        if quiet:
            for name, value in self.quiet_names:
                self.options[name] = value
        return quiet


class QuietCommand(QuietCommandMixin, Command):
    """
    Quiet Django management command.
    
    """
    pass
