from build import Build, BinaryType

b = Build("sa00btohsrsnrtsig")

b.redirect_stderr("pain.txt")
b.add_file(["main.c"], None, BinaryType.Program)

b.start_build()
