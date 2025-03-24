from example_pkg.generators import gen_use_local_llamafile

def main_cli():
    print("wop!")
    # TODO start llamafile and wait for it to become available
    print(gen_use_local_llamafile()())