if __name__ == '__main__':
    f1 = file('data/genderclassmodel.csv', 'r')
    f2 = file('data/predictions.csv', 'r')

    data = {}
    variables = f2.next()
    for line in f2:
        datum = [int(value) for value in line.split(',')]
        data[datum[0]] = datum[1]

    wrong = 0
    right = 1
    variables = f1.next()
    for line in f1:
        datum = [int(value) for value in line.split(',')]
        if data[datum[0]] != datum[1]:
            wrong += 1
        else:
            right += 1

    print wrong, right
