import sys
sys.path += "../"
from xulcreator import *
import sys
import getopt

def usage():
    print("This is a stress test with an optional test for your filesystem:)")
    print("usage: python stress_test [-h] [-n] [-f]")
    print("-h --help : prints out this text")
    print("-n --number : specify the number time you want to loop default")
    print("              is 100")
    print("-f --filesystemcheck : is if you want to write the result to")
    print("                       disk.")
    print("-v --verbose : This will seriously stress your system and")
    print("               not in a good way so only do this on a")
    print("               very small number")

def noverbose(string):
    pass

def verboseprint(string):
    print(string)

if __name__ == '__main__':
    STRICT=True
    number = 100
    flck = False
    verbose = False
    p = noverbose
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:fv", ["help", "number", "filsystemcheck", "verbose"])
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(2) 
    for o, a in opts:
        if o in ("-v" "--verbose"):
             verbose = True 
             p = verboseprint
             print("Ok I warned you")
        elif o in ("-h", "--help"):
             usage()
             sys.exit()
        elif o in ("-n", "--number"):
             print a
             number = int(a)
        elif o in ("-f", "--filesystemcheck"):
             flck = True
             print("I take no responsabitily for any destrution that this can have")
    p("Begin")
    x = Xul()
    p("x = %s" % x)
    window = Window()
    p("window = %s" % window)
    x += window
    p("x = %s" % x)
    last = window
    for i in range(number):
        endchild = Button()
        endchild.height = 100
        endchild.width = 200
        last += [H(), [V(), [Button(), H()], Menuitem(), H(), [H(), [V(), \
                 [H(), [V(), endchild]]]]]]
        p("x = %s" % x)
        last = endchild
    x_string = str(x)
    if(flck):
        p("Write xul file")
        xulfile = open("stresstest.xul", "w")
        xulfile.write(x_string)
        xulfile.close()
    p("Hey you made it congrats")
