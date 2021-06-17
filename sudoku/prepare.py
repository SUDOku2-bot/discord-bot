import glob


def cogs_modules(path: str) -> list:
    return [file.replace("./", "").replace("/", ".")[:-3] for file in glob.glob(f"{path}/*.py") if
            "__init__" not in file]
