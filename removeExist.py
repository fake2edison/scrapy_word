if __name__ == '__main__':
    file = open('2.txt', 'r', encoding="utf8")

    context = file.readlines()
    temp = []
    temp2 = []

    for i in context:
        # modifyWord(i.replace('\n', ''))
        temp.append(i)
    for i in temp:
        if i not in temp2:
            temp2.append(i)
    for s in temp2:
        print(s, end='')
    file.close()
