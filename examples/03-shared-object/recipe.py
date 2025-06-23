from build import Build, BinaryType

b = Build("test")

b.add_file(["main.c"], [b.yield_objname("max")], BinaryType.Program)
b.add_file(["max.c"], None, BinaryType.SharedObject)

b.start_build()
