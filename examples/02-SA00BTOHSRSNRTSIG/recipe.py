from build import Build

b = Build("sa00btohsrsnrtsig")

b.redirect_stderr("pain.txt")
b.add_file(["main.c"], is_object=False)

b.start_build()
