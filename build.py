import os
import subprocess as sp

from io import TextIOWrapper
from typing import Any
from enum import Enum

import sys
from typing_extensions import TextIO

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
        self.task_queue_index: int = 0

        self.message = Messages()
        self.stderr = sys.stderr
        self.stderr_changed = False

    def redirect_stderr(self, filename) -> None:
        self.message.put_message(Messages.Prefix.Meta, f"Redirecting stderr to {filename}")
        self.stderr = open(filename, 'a')
        self.stderr_changed = True

    @staticmethod
    def repurpose_stderr(stderr: TextIO | Any, mode: str = "a") -> Any:
        if type(stderr) == str:
            return open(stderr, mode)

        if not stderr.closed:
            stderr.close()
            return open(stderr.name, mode)

    def override_default_compiler(self, compiler_name: str) -> None:
        self.compiler = compiler_name

    def add_compiler_arguments(self, arguments: str | list) -> None:
        if type(arguments) == str:
            self.global_cc_flags.append(arguments)
            return

        for argument in arguments:
            self.global_cc_flags.append(argument)

    def add_task_queue(self, arguments: list) -> None:
        self.task_queue[str(self.task_queue_index)] = arguments
        self.task_queue_index += 1

    def add_file(self, file: str | list, dependencies: str | list | None = None, **kwargs) -> None:
        if not dependencies:
            dependencies = ""

        if not kwargs["is_object"]:

            # BUG: when add_file()'s first parameter is put as a string,
            #      it will split the string into characters (lol)
            # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            if not self.global_cc_flags and not dependencies:
                self.add_task_queue(
                    [
                        self.compiler,
                        "-o",
                        self.program_name,
                        " ".join(file),
                    ]
                )
                return

            self.add_task_queue(
                [
                    self.compiler,
                    "-o",
                    self.program_name,
                    " ".join(file),
                    " ".join(self.global_cc_flags),
                    dependencies
                ]
            )
            return

            # -------------------------y

        # do object files need dependencies?
        #   - ANSWER THAT QUESTION ON GITHUB ISSUES!

        if not self.global_cc_flags:
            self.add_task_queue(
                [
                    self.compiler,
                    "-c",
                    " ".join(file),
                ]
            )
            return

        self.add_task_queue(
            [
                self.compiler,
                "-c",
                " ".join(file),
                " ".join(self.global_cc_flags)
            ]
        )

    def add_resource(self, resource_intepreter: str, resource_intepreter_arguments: list) -> None:
        self.add_task_queue([resource_intepreter, resource_intepreter_arguments])

    # TODO: time-based building so we don't rebuild the entire thing
    def start_build(self):
        # ~~BUG: multiple file builds cannot be possible yet.~~
        #   - FIXED! (may 26, 2025 - 10:42 pm)
        for task_queues in reversed(self.task_queue):
            cleaned_command_line = list(filter(None, self.task_queue[task_queues]))

            # self.message.put_message(Messages.Prefix.CompilerMessage, f"Uncut command line: {self.task_queue[task_queues]}")
            self.message.put_message(Messages.Prefix.CompilerMessage, " ".join(cleaned_command_line))
            # self.message.put_message(Messages.Prefix.CompilerMessage, f"Cut command line: {cleaned_command_line}")

            process = sp.Popen(
                cleaned_command_line, stdout=sp.PIPE, stderr=self.stderr
            )

            # wait for process so we get return code
            process.wait()

            if process.returncode != 0:
                # btw, we still have to read from self.stderr...
                if not self.stderr_changed:
                    self.message.put_message(Messages.Prefix.CompilerError, "Compilation failed!")

                    # close and reopen self.stderr for reading instead
                    self.stderr = Build.repurpose_stderr(self.stderr, 'r')
                    self.message.put_message(Messages.Prefix.CompilerError, self.stderr.read())
                    self.stderr.close()

                    return

                self.message.put_message(Messages.Prefix.CompilerError, "Compilation failed!")

                # close and reopen self.stderr for reading instead
                self.stderr = Build.repurpose_stderr(self.stderr, 'r')
                self.message.put_message(Messages.Prefix.Meta, f"NOTE: you redirected stderr to {self.stderr.name}")
                self.stderr.close()

                return

            continue

        self.message.put_message(Messages.Prefix.Meta, "---- Compilation finished ----")
