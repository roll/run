import unittest
from io import StringIO
from unittest.mock import patch
from run import Module, FunctionTask, require, trigger
#TODO: Nose in shell imports module instead of object
from run.task import task

#Tests

class DependencyTest(unittest.TestCase):
    
    #Public

    def setUp(self):
        self.patcher = patch('sys.stdout', new_callable=StringIO)
        self.stdout = self.patcher.start()
        self.addCleanup(patch.stopall)         
        self.module = MockMainModule(meta_module=None)
        
    def test_list(self):
        self.module.list()
        self.assertEqual(
            self.stdout.getvalue(), 
            'default\n'
            'info\n'
            'list\n'
            'meta\n'
            'task1\n'
            'task2\n'
            'task3\n'
            'task4\n'
            'task5\n') 
        
    def test_task3(self):
        self.module.task3()
        self.assertEqual(
            self.stdout.getvalue(), 
            'task1 is done\n'
            'task3 is done\n'
            'task2 is done\n')
        
    def test_task4(self):
        self.module.task4()
        self.assertEqual(
            self.stdout.getvalue(), 
            'task1 is done\n'
            'task4 is done\n'
            'task2 is done\n')
        
    def test_task5(self):
        self.module.task5()
        self.assertEqual(
            self.stdout.getvalue(), 
            'task1 is done\n'
            'task5 is done\n'
            'task2 is done\n')                                  


#Fixtures

class MockMainModule(Module):
    
    #Tasks
    
    def task1(self):
        print('task1 is done')
    
    def task2(self):
        print('task2 is done')
        
    task3 = FunctionTask(
        function=lambda: print('task3 is done'),
        require=['task1'],
        trigger=['task2'],
    )
    
    @require('task1')
    @trigger('task2')
    def task4(self):
        print('task4 is done')
    
    @task
    def task5(self):
        print('task5 is done')
      
    task5.require('task1')
    task5.trigger('task2')