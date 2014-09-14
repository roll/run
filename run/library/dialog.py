from dialog import Dialog
from ..task import FunctionTask
from ..var import Var


# TODO: rebase from FunctionTask?
class DialogTask(FunctionTask):

    # Public

    def __init__(self, *args, **kwargs):
        self.__dialog = Dialog()
        if kwargs.get('message', False):
            function = self.__dialog.message
        elif kwargs.get('question', False):
            function = self.__dialog.question
        else:
            raise ValueError('Unsupported mode')
        super().__init__(function, *args, **kwargs)


class DialogVar(Var, DialogTask): pass