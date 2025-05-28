import build
from build import BinaryType as bt

b = build.Build("hello")

b.override_default_compiler("gcc")
b.add_compiler_arguments(["-std=c99"])
b.add_file(["main.c"], None, bt.Program)

b.start_build()
