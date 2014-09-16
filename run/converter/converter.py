from abc import ABCMeta, abstractmethod
from box.functools import Decorator
from .result import Result
from .skip import skip


class Converter(Decorator, metaclass=ABCMeta):
    """Base abstract converter decorator.
    """

    # Public

    def __init__(self, **kwargs):
        self.__kwargs = kwargs

    def __call__(self, obj):
        if self.__check_converted(obj):
            return obj
        if self.__check_eligible(obj):
            if self._match(obj):
                return self._make(obj)
        raise TypeError(
            'Converter "{self}" is not suitable converter '
            'for the given object "{obj}" convertation.'.
            format(self=self, obj=obj))

    # Protected

    # override
    def _is_composite(self, *args, **kwargs):
        # Composite only if args not passed
        return not bool(args)

    @abstractmethod
    def _match(self, obj):
        pass  # pragma: no cover

    @abstractmethod
    def _make(self, obj):
        pass  # pragma: no cover

    @property
    def _kwargs(self):
        return self.__kwargs

    # Private

    __kwargs = {}

    def __check_converted(self, obj):
        return isinstance(obj, Result)

    def __check_eligible(self, obj):
        if isinstance(obj, staticmethod):
            return False
        if isinstance(obj, classmethod):
            return False
        if getattr(obj, skip.attribute_name, False):
            return False
        return True
