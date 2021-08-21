from glob import glob

path = glob("./lib/cogs/*.py")

def get_cogs():
    # 파일명 얻기
    filenames = [path.split("\\")[-1] for path in glob("./lib/cogs/*.py")]
    # 확장자 제거
    filenames = list(map(lambda f: f[:-3], filenames))
    # __init__ 제거
    filenames.remove("__init__")

    return filenames

print(get_cogs())
