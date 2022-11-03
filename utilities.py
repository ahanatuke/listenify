

def paginate(items, num = 5):
    '''items: list of ONLY displayable items, do not pass in your ugly 3dim array Anya
        num: number of items per page, defaults to 5'''
    maxIndex = len(items) - 1
    if (maxIndex+1)%5 == 0:
        numPages = int((maxIndex+1)/5)
    else:
        numPages = int(maxIndex/5)

    pageNum = 0
    if (maxIndex+1) < num:
        num = maxIndex+1

    pageIndices = []
    for i in range(1,num+1):
        pageIndices.append(str(i))


    print("Enter 'N' to go to the next page. Enter 'P' to go to the previous page.\n"
          "Enter a number from 1 to "+str(num)+" to select that result. Press Enter to quit")

    while True:
        if pageNum == numPages:
            for i in range(0, (maxIndex+1)%5):
                print(items[(5 * pageNum) + i])
            print("Page " + str(pageNum+1) + " / " + str(numPages+1))
        else:
            for i in range(0,num):
                print(items[(5*pageNum) + i])
            print("Page " + str(pageNum+1) +" / " + str(numPages+1))

        while True:
            userInput = input("> ")
            if userInput == "":
                #quit
                return None
            elif userInput.strip().lower() == 'p':
                if pageNum > 0:
                    pageNum -= 1
                break
            elif userInput.strip().lower() == 'n':
                if pageNum < numPages:
                    pageNum += 1
                break
            elif userInput.strip() in pageIndices:
                return (5*pageNum) + int(userInput.strip()) - 1
            else:
                print("Invalid input, please try again or press Enter to quit.")


'''items = [[81, 60, 3, 32, 86, 9, 2, 76, 79, 11],
         [39, 43, 85, 96, 42, 44, 62, 11, 11, 53],
         [96, 64, 30, 96, 12, 51, 98, 77, 13, 77],
         [76, 46, 39, 22, 79, 6, 76, 59, 7, 63],
         [58, 19, 37, 53, 60, 99, 52, 79, 39, 67],
         [95, 9, 82, 14, 91, 31, 90, 27, 42, 55],
         [23, 50, 66, 30, 90, 76, 36, 34, 87, 55],
         [31, 69, 16, 24, 18, 33, 64, 6, 94, 31],
         [70, 51, 46, 76, 3, 74, 2, 21, 20, 18],
         [54, 38, 80, 78, 66, 25, 27, 36, 80, 39],
         [1, 66, 40, 57, 18, 56, 6, 35, 30, 60],
         [98, 12, 61, 44, 59, 36, 18, 46, 30, 79],
         [37, 84, 20, 57, 83, 75, 4, 83, 32, 21],
         [59, 34, 64, 13, 8, 1, 22, 52, 10, 27],
         [68, 78, 24, 33, 23, 85, 76, 69, 74, 31],
         [44, 50, 50, 27, 98, 8, 96, 77, 18, 75],
         [50, 87, 21, 11, 88, 8, 36, 29, 80, 56]]'''

#paginate(items)