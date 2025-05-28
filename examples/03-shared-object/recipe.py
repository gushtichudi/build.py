from build import Build, BinaryType

b = Build("test")

b.add_file(["main.c"], ["max.so"], BinaryType.Program)
b.add_file(["max.c"], None, BinaryType.SharedObject)

b.start_build()
