def occurrences(search, text):
    count = 0
    start = 0
    while True:
        start = text.find(search, start)
        if start == -1:
            return count
        count += 1
        start += 1

def main():
    ret = occurrences('aa', 'aaaaa')
    ret = occurrences('ab', 'ababa')

    pass

if __name__ == '__main__':
    main()