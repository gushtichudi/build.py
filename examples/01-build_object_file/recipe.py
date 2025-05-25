from build import Build

b = Build("love")

b.override_default_compiler("gcc")
b.add_file(["main.c"], "less.o", is_object=False)
b.add_file(["less.c"], is_object=True)

b.start_build()
