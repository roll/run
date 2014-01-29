from abc import ABCMeta, abstractmethod
from ..dependent import DependentAttributeBuilder
from .method import MethodTask       

class TaskDependency(metaclass=ABCMeta):
    
    #Public
    
    def __init__(self, tasks):
        self._tasks = tasks
    
    def __call__(self, method):
        if isinstance(method, self._builder_class):
            builder = method
        else:
            builder = self._attribute_class(method)
        self._apply_dependency(builder)
        return builder
    
    #Protected
    
    _builder_class = DependentAttributeBuilder
    _attribute_class = MethodTask
    
    @abstractmethod
    def _apply_dependency(self, builder):
        pass #pragma: no cover


class require(TaskDependency):
    
    #Protected
    
    def _apply_dependency(self, builder):
        builder.require(self._tasks)


class trigger(TaskDependency):
    
    #Protected
    
    def _apply_dependency(self, builder):
        builder.trigger(self._tasks)