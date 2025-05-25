import os
import subprocess as sp

from typing import Any
from enum import Enum

import sys

class Messages:
    class Prefix(Enum):
        CompilerMessage = 0
        Meta            = 1
        CompilerError   = 2

    def __init__(self, redirect_output: Any = None):
        self.redirect_output = redirect_output

    def put_message(self, kind: Prefix, msg: str) -> None:
        match kind:
            case Messages.Prefix.CompilerMessage:
                if not self.redirect_output:
                    sys.stderr.write(f"[CC] {msg}\n")
                    return

                with open(self.redirect_output, 'a') as file:
                    file.write(f"[CC] {msg}\n")
                    return

            case Messages.Prefix.Meta:
                if not self.redirect_output:
                    sys.stderr.write(f"[!!] {msg}\n")
                    return

                with open(self.redirect_output, 'a') as file:
                    file.write(f"[!!] {msg}\n")
                    return

            case Messages.Prefix.CompilerError:
                if not self.redirect_output:
                    sys.stderr.write(f"[EE] {msg}\n")
                    return

                with open(self.redirect_output, 'a') as file:
                    file.write(f"[EE] {msg}\n")
                    return

class Build:
    def __init__(self, program_name):
        self.program_name = program_name
        self.compiler = "cc" # by default
        self.global_cc_flags: list = []   # every file has it

        self.task_queue: dict = {}

        self.message = Messages()
        self.stderr = sys.stderr
        self.stderr_changed = False

    def redirect_stderr(self, filename) -> None:
        self.message.put_message(Messages.Prefix.Meta, f"Redirecting stderr to {filename}")
        self.stderr = open(filename, 'a')
        self.stderr_changed = True

    def override_default_compiler(self, compiler_name: str) -> None:
        self.compiler = compiler_name

    def add_compiler_arguments(self, arguments: str | list) -> None:
        if type(arguments) == str:
            self.global_cc_flags.append(arguments)
            return

        for argument in arguments:
            self.global_cc_flags.append(argument)

    def add_task_queue(self, arguments: list) -> None:
        idx: int = 0

        self.task_queue[str(idx)] = arguments
        idx += 1

    def add_file(self, file: str | list, dependencies: str | list | None = None, **kwargs) -> None:
        if not dependencies:
            dependencies = ""

        if not kwargs["is_object"]:

            # BUG: when add_file()'s first parameter is put as a string,
            #      it will split the string into characters (lol)
            # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            self.add_task_queue(
                [
                    self.compiler,
                    "-o",
                    self.program_name,
                    " ".join(file),
                    " ".join(self.global_cc_flags),
                ]
            )
            return

        self.add_task_queue(
            [
                self.compiler,
                "-c",
                " ".join(file),
                "-o",
                " ".join(file).split('.')[0],
                " ".join(self.global_cc_flags)
            ]
        )

    def add_resource(self, resource_intepreter: str, resource_intepreter_arguments: list) -> None:
        self.add_task_queue([resource_intepreter, resource_intepreter_arguments])

    # TODO: time-based building so we don't rebuild the entire thing
    def start_build(self):
        # BUG: multiple file builds cannot be possible yet.
        for task_queues in reversed(self.task_queue):
            cleaned_command_line = list(filter(None, self.task_queue[task_queues]))

            self.message.put_message(Messages.Prefix.CompilerMessage, f"Uncut command line: {self.task_queue[task_queues]}")
            self.message.put_message(Messages.Prefix.CompilerMessage, " ".join(self.task_queue[task_queues]))
            self.message.put_message(Messages.Prefix.CompilerMessage, f"Cut command line: {cleaned_command_line}")

            process = sp.Popen(
                cleaned_command_line, stdout=sp.PIPE, stderr=self.stderr
            )

            # wait for process so we get return code
            process.wait()

            # if compilation fails, also get error codes
            out, err = process.communicate()

            if process.returncode != 0:
                if not self.stderr_changed:
                    self.message.put_message(Messages.Prefix.CompilerError, "Compilation failed!")

                    if err == None:
                        self.message.put_message(Messages.Prefix.Meta, "Cannot fetch error message")

                    return

                self.message.put_message(Messages.Prefix.CompilerError, "Compilation failed!")
                self.message.put_message(Messages.Prefix.CompilerError, self.stderr.read())
                self.stderr.close()

                return

            self.message.put_message(Messages.Prefix.Meta, f"---- Compilation finished for task queue {task_queues} ----")
            continue
