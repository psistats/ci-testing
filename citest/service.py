import time

def main():
    x = 0
    while True:
        print("counter: %s" % x)
        x = x + 1
        time.sleep(1)

if __name__ == "__main__":
    main()
