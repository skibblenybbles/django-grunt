import optparse

from django.core.management import base


class Command(base.BaseCommand):
    """
    Base class for a declarative management command API.
    
    """
    option_list = ()
    option_groups = ()
    option_names = ()
    actions = ()
    
    def usage(self, subcommand):
        """
        Override the usage display.
        
        """
        usage = "%prog {subcommand:s} {args:}".format(
            subcommand=subcommand, args=self.args)
        if self.help:
            return "{usage:s}\n\n{help:s}".format(
                usage=usage, help=self.help)
        return usage
    
    def create_parser(self, prog_name, subcommand):
        """
        Customize the OptionParser.
        
        """
        parser = super(Command, self).create_parser(prog_name, subcommand)
        for name, description, option_list in self.option_groups:
            group = optparse.OptionGroup(parser, name, description);
            map(group.add_option, option_list)
            parser.add_option_group(group)
        return parser
    
    def parse_options(self):
        for name in self.option_names:
            parse = getattr(self, "parse_option_{name:s}".format(
                name=name), None)
            if parse is not None and callable(parse):
                self.options[name] = parse()
    
    def handle(self, *args, **options):
        self.args = args
        self.options = options
        self.parse_options()
        
        for name in self.actions:
            validate = getattr(self, "validate_{name:s}".format(
                name=name), None)
            if validate is not None and callable(validate):
                validate()
        for name in self.actions:
            handle = getattr(self, "handle_{name:s}".format(
                name=name), None)
            if handle is not None and callable(handle):
                handle()


class BaseCommandMixin(object):
    """
    Base Django management command options.
    
    """
    option_list = base.BaseCommand.option_list
    option_groups = (
        ("[standard options]",
            "Standard Django management command options.",
            option_list,
        ),
    )
    option_names = ("verbosity",)
    actions = ()
    
    def parse_option_verbosity(self):
        try:
            verbosity = int(self.options.get("verbosity", 1))
        except (ValueError, TypeError):
            verbosity = 1
        return verbosity


class BaseCommand(BaseCommandMixin, Command):
    """
    Base Django management command.
    
    """
    pass
