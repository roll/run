import os
import sys
import inspect
import logging.config
from clyde import Command, Option, mixin
from .helpers import cachedproperty, load, parse
from .module import Module
from .settings import settings
version = '0.47.0'  # REPLACE: version = '{{ version }}'


class Program(Command):
    """Run main program.
    """

    # Public

    def Execute(self, attribute=None, *arguments):
        for name in ['list', 'info', 'meta']:
            if getattr(self, name, False):
                if attribute is not None:
                    arguments = (attribute,) + arguments
                attribute = name
                break
        self.__run(attribute, *arguments)

    # Mixins

    @mixin
    def initiate_logging(self):
        logging.config.dictConfig(settings.logging_config)
        logger = logging.getLogger()
        if self.verbose:
            logger.setLevel(logging.DEBUG)
        if self.quiet:
            logger.setLevel(logging.ERROR)

    @mixin(require='help')
    def print_help(self):
        print(self.Format('help'))
        exit()

    @mixin(require='version')
    def print_version(self):
        print(version)
        exit()

    # Options

    filepath = Option(
        flags=['-f', '--filepath'],
        default=settings.filename,
        help='Runfile path.',
    )

    help = Option(
        action='store_true',
        flags=['-h', '--help'],
        help='Display this help message.',
    )

    info = Option(
        action='store_true',
        flags=['-i', '--info'],
        help='Display task information.',
    )

    list = Option(
        action='store_true',
        flags=['-l', '--list'],
        help='Display module tasks.',
    )

    meta = Option(
        action='store_true',
        flags=['-m', '--meta'],
        help='Display task meta.',
    )

    quiet = Option(
        action='store_true',
        flags=['-q', '--quiet'],
        help='Enable quiet mode.',
    )

    settings = Option(
        action='append',
        default=[],
        flags=['-s', '--settings'],
        help='Add settings key/value pair.',
    )

    verbose = Option(
        action='store_true',
        flags=['-v', '--verbose'],
        help='Enable verbose mode.',
    )

    version = Option(
        action='store_true',
        flags=['-V', '--version'],
        help='Display the program version.',
    )

    # Private

    def __run(self, attribute, *arguments):
        args, kwargs = parse(''.join(arguments))
        try:
            if attribute is None:
                attribute = self.__module
            else:
                attribute = getattr(self.__module, attribute)
            if not callable(attribute):
                return print(attribute)
            self.__update_settings()
            result = attribute(*args, **kwargs)
            if result is not None:
                print(result)
        except Exception as exception:
            logger = logging.getLogger(__name__)
            logger.error(str(exception), exc_info=self.verbose)
            sys.exit(1)

    @cachedproperty
    def __module(self):
        filepath = os.path.abspath(self.filepath)
        module = load(filepath)
        for name in dir(module):
            attr = getattr(module, name)
            if not isinstance(attr, type):
                continue
            if not issubclass(attr, Module):
                continue
            if inspect.getmodule(attr) != module:
                continue
            module = attr(Build=True)
            return module
        raise RuntimeError('Module not found.')

    def __update_settings(self):
        _, patch = parse(','.join(self.settings))
        for key, value in patch.items():
            setattr(settings, key, value)


program = Program(name='run')
