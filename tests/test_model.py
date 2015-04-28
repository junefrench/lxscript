from unittest import TestCase
from unittest.mock import Mock
from model.system import *


class SystemTest(TestCase):
    def test_output_system(self):
        output_function = Mock()
        s = OutputSystem(output_function)
        s.set_level(0.5)
        output_function.assert_called_once_with(0.5)

    def test_compound_system(self):
        of1 = Mock()
        of2 = Mock()
        of3 = Mock()
        cs = CompoundSystem([
            OutputSystem(of1),
            CompoundSystem([
                OutputSystem(of2),
                OutputSystem(of3)
            ])
        ])
        cs.set_level(0.25)
        for of in [of1, of2, of3]:
            of.assert_called_once_with(0.25)
