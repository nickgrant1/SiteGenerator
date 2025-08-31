import os, shutil


def main():
    move_contents('one', 'l')


def move(src, dest):
    for thing in os.listdir(src):
        path = os.path.join(src, thing)
        if os.path.isdir(path):
            move(path, dest)
        else:
            shutil.copy(path, dest)
        

def move_contents(src, dest):
    destination = os.path.abspath(dest)
    #shutil.rmtree(destination)   #clean folder
    #os.mkdir(destination)

    cwd = os.getcwd()
    source = os.path.join(cwd, src)
    #move(source, destination)
    print(os.path.abspath('AIagent'))



if __name__ == "__main__":
    main()
