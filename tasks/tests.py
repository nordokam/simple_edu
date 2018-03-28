import unittest
from pathlib import Path
from django.core.files.base import ContentFile

from .utils import check_code, test_code
from .models import TestCase, Task, TestInOut


class CheckCodeTestCase(unittest.TestCase):

    def setUp(self):
        with open('valid_test_code.py', 'w+') as valid_file:
            valid_file.write("def foo():\n    pass\n")
        self.valid_code_path = Path.cwd().joinpath(valid_file.name)

        with open('invalid_test_code.py', 'w+') as invalid_file:
            invalid_file.write("foo(")
        self.invalid_code_path = Path.cwd().joinpath(invalid_file.name)

    def test_valid_code(self):
        errors, valid = check_code(
            str(self.valid_code_path.absolute()))
        self.assertTrue(valid)
        self.assertEqual(errors, [])

    def test_invalid_code(self):
        errors, valid = check_code(
            str(self.invalid_code_path.absolute()))
        self.assertFalse(valid)
        self.assertEqual(len(errors), 2)

    def tearDown(self):
        self.valid_code_path.unlink()
        self.invalid_code_path.unlink()


class TestCodeTestCode(unittest.TestCase):

    def setUp(self):
        invalid_file = ContentFile(
            'if __name__ == "__main__": \n'
            '    new_sum = 0 \n'
            '    for i in range(0, 2):\n'
            '        new_sum += input()\n'
            '    print(new_sum+1)\n')
        invalid_task = Task.objects.create(title='invalid_test')
        invalid_task.file.save('invalid_file.py', invalid_file)
        test_case1 = TestCase.objects.create(title='test1', task=invalid_task)
        TestInOut.objects.create(test_case=test_case1, value=1)
        TestInOut.objects.create(test_case=test_case1, value=1)
        TestInOut.objects.create(test_case=test_case1, value=2, is_input=False)

        valid_file = ContentFile(
            'if __name__ == "__main__": \n'
            '    new_sum = 0 \n'
            '    for i in range(0, 2):\n'
            '        new_sum += int(input())\n'
            '    print(new_sum)\n')
        valid_task = Task.objects.create(title='valid_test')
        valid_task.file.save('valid_file.py', valid_file)
        test_case2 = TestCase.objects.create(title='test2', task=valid_task)
        TestInOut.objects.create(test_case=test_case2, value=1)
        TestInOut.objects.create(test_case=test_case2, value=1)
        TestInOut.objects.create(test_case=test_case2, value=2, is_input=False)

    def test_valid_code(self):
        invalid_task = Task.objects.get(title='invalid_test')
        errors, valid = test_code(invalid_task.id)
        self.assertEqual(len(errors), 1)
        self.assertEqual(valid, False)

        valid_task = Task.objects.get(title='valid_test')
        errors, valid = test_code(valid_task.id)
        self.assertEqual(len(errors), 0)
        self.assertEqual(valid, True)

    def tearDown(self):
        Task.objects.filter(title='invalid_test').delete()
        Task.objects.filter(title='valid_test').delete()
