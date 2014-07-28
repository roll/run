import unittest
from unittest.mock import Mock
from run.attribute.prototype import AttributePrototype

class AttributePrototypeTest(unittest.TestCase):

    # Public

    def setUp(self):
        self.set = Mock(apply=Mock())
        self.call = Mock(apply=Mock())
        self.updates = []
        self.args = ('arg1',)
        self.kwargs = {'kwarg1': 'kwarg1'}
        self.Attribute = self._make_mock_attribute_class()
        self.Prototype = self._make_mock_prototype_class(self.set, self.call)
        self.prototype = self.Prototype(
            self.Attribute, self.updates, *self.args, **self.kwargs)

    def test___getattr__(self):
        self.assertEqual(self.prototype.attr1, 'value1')

    def test___getattr___no_attribute(self):
        self.assertEqual(self.prototype.attr2, self.prototype)

    def test___setattr__(self):
        self.prototype.attr3 = 'value3'
        self.prototype._set_class.assert_called_with('attr3', 'value3')
        self.assertEqual(self.updates, [self.set])

    def test___call__(self):
        result = self.prototype.attr4(*self.args, **self.kwargs)
        self.assertEqual(result, self.prototype)
        self.prototype._call_class.assert_called_with(
            'attr4', *self.args, **self.kwargs)
        self.assertEqual(self.updates, [self.call])

    def test___copy__(self):
        self.prototype.attr3 = 'value3'
        self.prototype.attr4(*self.args, **self.kwargs)
        copied_prototype = self.prototype.__copy__('arg2', kwarg2='kwarg2')
        self.assertIsInstance(copied_prototype, self.Prototype)
        self.assertEqual(copied_prototype._class, self.Attribute)
        self.assertEqual(copied_prototype._updates, [self.set, self.call])
        self.assertEqual(copied_prototype._args, ('arg1', 'arg2'))
        self.assertEqual(copied_prototype._kwargs,
            {'kwarg1': 'kwarg1', 'kwarg2': 'kwarg2'})

    def test___build__(self):
        self.prototype.attr3 = 'value3'
        self.prototype.attr4(*self.args, **self.kwargs)
        attribute = self.prototype.__build__('module')
        self.assertIsInstance(attribute, self.Attribute)
        attribute.__build__.assert_called_with(
            'module', *self.args, **self.kwargs)
        self.set.apply.assert_called_with(attribute)
        self.call.apply.assert_called_with(attribute)

    # Protected

    def _make_mock_attribute_class(self):
        class MockAttribute:
            # Public
            __build__ = Mock()
            attr1 = 'value1'
        return MockAttribute

    def _make_mock_prototype_class(self, st, call):
        class MockPrototype(AttributePrototype):
            # Protected
            _set_class = Mock(return_value=st)
            _call_class = Mock(return_value=call)
        return MockPrototype