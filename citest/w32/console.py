from citest.win_business import WinBusiness

if __name__ == "__main__":
    b = WinBusiness()
    for x in range(0, 10):
        b.run()
        print("x: %s - counter %s" % (x, b.counter))
    main()
    input("Press enter to continue...")
