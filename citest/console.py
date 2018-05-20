from citest.business import Business

def main():

    b = Business()

    print("Current Counter: %s" % b.counter)

    for x in range(0,10):
        b.run(x)
        print("x: %s - counter: %s" % (x, b.counter))

