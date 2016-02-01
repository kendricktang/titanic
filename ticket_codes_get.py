from csv import reader


if __name__ == '__main__':
    f = file('data/train_titles_tickets.csv', 'r')

    lines = reader(f)
    atts = lines.next()

    codes = []

    for line in lines:
        code = line[9]
        if code not in codes:
            codes.append(code)
    f.close()

    f = file('ticket_codes.py', 'w')
    f.write('ticket_codes = ')
    f.write(str(codes))
