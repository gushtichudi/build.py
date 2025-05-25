import build

b = build.Build("hello")

b.override_default_compiler("gcc")
b.add_compiler_arguments(["-std=c99"])
b.add_file(["main.c"], is_object=False)

b.start_build()
