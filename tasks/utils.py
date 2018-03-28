from pathlib import Path
from flake8.api import legacy as flake8
from .models import Task
from .container import Sandbox

def check_code(file_path):
    """
    Basic code check with flake8
    :param file_path:
    :return: errors list and bool(valid/invalid)
    """
    valid = False
    errors = []
    if all([Path(file_path).exists(), Path(file_path).is_file(),
            file_path.endswith('.py')]):
        style_guide = flake8.get_style_guide(ignore=['E24', 'W503'])
        report = style_guide.check_files([file_path])
        errors = report.get_statistics('')
        valid = len(errors) == 0

    return errors, valid


def test_code(task_id):
    """
    Testing code in docker container
    :param task_id: Task id
    :return: list of errors and valid/invalid
    """
    errors = []
    valid = True
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return ['Code file does not exist'], False
    else:
        # our docker sandbox
        with Sandbox() as sandbox:
            for num, case in enumerate(task.cases.all(), start=1):
                input_data = ''
                for item in case.get_input_items():
                    input_data += '{}\n'.format(item.value)
                sandbox.add_files(task.file.file.name)
                code_output = sandbox.run_command(['python', task.file.name],
                                                  timeout=100,
                                                  input_data=input_data)
                code_errors = code_output.stderr.read().decode()
                # check for code errors
                if code_errors:
                    valid = False
                    errors.append(code_errors)
                else:
                    # compare code output and code expected output
                    code_output = code_output.stdout.read().decode().split('\n')
                    code_output = [x for x in code_output if x]
                    expected_output = []
                    for item in case.get_output_items():
                        expected_output.append(item.value)
                    if code_output != expected_output:
                        valid = False
                        code_output = ''.join(code_output)
                        expected_output = ''.join(expected_output)
                        msg = ('Case {}: Output data mismatch: expect this: {} '
                               'got this: {}'.format(
                                num, expected_output, code_output))
                        errors.append(msg)

    return errors, valid
