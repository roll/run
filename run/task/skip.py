from sugarbowl import Function


class skip(Function):
    """Make object to be not converted while convert call.

    Examples
    --------
    Usage example::

      class Module(Module):

          @skip
          def method(self):
              pass

    In this case method will not be converted to run's task and
    will stay as regular python method.
    """

    # TODO: rename to marker
    attribute_name = '_run_task_skip'
    protocol = Function.FUNCTION

    def __call__(self, obj):
        setattr(obj, self.attribute_name, True)
        return obj
