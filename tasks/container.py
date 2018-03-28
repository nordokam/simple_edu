import json
import subprocess
import tempfile
from io import FileIO
from typing import List

from autograder_sandbox import AutograderSandbox


class CompletedCommand:
    def __init__(self, return_code: int, stdout: FileIO, stderr: FileIO,
                 timed_out: bool,
                 stdout_truncated: bool, stderr_truncated: bool):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.timed_out = timed_out
        self.stdout_truncated = stdout_truncated
        self.stderr_truncated = stderr_truncated


class Sandbox(AutograderSandbox):

    def run_command(self,
                    args: List[str],
                    max_num_processes: int=None,
                    max_stack_size: int=None,
                    max_virtual_memory: int=None,
                    as_root: bool=False,
                    stdin: FileIO=None,
                    timeout: int=None,
                    check: bool=False,
                    truncate_stdout: int=None,
                    truncate_stderr: int=None,
                    input_data: str=None) -> 'CompletedCommand':
        cmd = ['docker', 'exec', '-i', self.name, 'cmd_runner.py']

        if timeout is not None:
            cmd += ['--timeout', str(timeout)]

        cmd += args

        with tempfile.TemporaryFile() as f:
            try:
                subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE,
                               check=True, input=input_data, encoding='ascii')
                f.seek(0)
                json_len = int(f.readline().decode().rstrip())
                results_json = json.loads(f.read(json_len).decode())

                stdout_len = int(f.readline().decode().rstrip())
                stdout = tempfile.NamedTemporaryFile()
                stdout.write(f.read(stdout_len))
                stdout.seek(0)

                stderr_len = int(f.readline().decode().rstrip())
                stderr = tempfile.NamedTemporaryFile()
                stderr.write(f.read(stderr_len))
                stderr.seek(0)

                result = CompletedCommand(return_code=results_json['return_code'],  # noqa
                                          timed_out=results_json['timed_out'],
                                          stdout=stdout,
                                          stderr=stderr,
                                          stdout_truncated=results_json['stdout_truncated'],  # noqa
                                          stderr_truncated=results_json['stderr_truncated'])  # noqa

                if (result.return_code != 0 or results_json['timed_out']) and check:  # noqa
                    raise subprocess.CalledProcessError(
                        result.return_code, cmd,
                        output=result.stdout, stderr=result.stderr)

                return result
            except subprocess.CalledProcessError as e:
                f.seek(0)
                print(f.read())
                print(e.stderr)
                raise
