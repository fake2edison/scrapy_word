def modifyWord(word):
    temp = ""
    str = word.split('+')
    for s in str:
        s = trim(s)
        if s.isupper() and s == ''.join(s.split()):
            temp = temp + '(' + s + '*china)+'
        else:
            temp = temp + '(' + s + ')+'
    temp = temp.replace('-', '\-')
    print(temp[0:-1])


def trim(s):
    if len(s) == 0:
        return s
    elif s[0] == ' ' or s[0] == '\n':
        return (trim(s[1:]))
    elif s[-1] == ' ' or s[-1] == '\n':
        return (trim(s[:-1]))
    return s


if __name__ == '__main__':

    file = open('3.txt', 'r', encoding="utf8")

    context = file.readlines()

    for i in context:
        modifyWord(i.replace('\n', ''))

    file.close()
