import unittest
from unittest.mock import Mock, call
from run.task.task import Task

#Tests

class TaskTest(unittest.TestCase):

    #Public

    def setUp(self):
        self.task = MockTask(module=None)

    def test___get__(self):
        self.assertEqual(self.task.__get__('module'), self.task)
        
    def test___set__(self):
        value = lambda: 'value'
        self.task.__set__('module', value)
        self.assertEqual(self.task.complete, value)
        
    def test___set___not_callable(self):
        self.assertRaises(TypeError, self.task.__set__, 'module', 'value')        
        
    def test___call__(self):
        self.assertEqual(self.task.__call__(), 'value')
        self.task.complete.assert_called_with()
        self.task._initiated_signal_class.assert_called_with(self.task)
        self.task._retrieved_signal_class.assert_called_with(self.task)
        self.task._dispatcher.add_signal.assert_has_calls(
            [call('initiated_signal'), call('retrieved_signal')])
        
    def test_complete(self):
        task = Task(module=None)
        self.assertEqual(task.complete(), None)

    
#Fixtures

class MockTask(Task):
    
    #Public
    
    complete = Mock(return_value='value')

    #Protected

    _dispatcher = Mock(add_signal = Mock())
    _initiated_signal_class = Mock(return_value='initiated_signal')
    _retrieved_signal_class = Mock(return_value='retrieved_signal')    