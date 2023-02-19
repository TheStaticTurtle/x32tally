import glob
import base64

with open("x32icons.css", "w") as f:
    for file in glob.glob("x32*.png"):
        data = open(file, "rb").read()
        data = base64.b64encode(data)
        data = data.decode("utf-8")
        name = file.replace("_", "-").replace(".png", "")
        f.write(f".{name} {{\n")
        f.write(f"    background: url(\"data:image/png;base64,{data}\");\n")
        f.write(f"}}\n")