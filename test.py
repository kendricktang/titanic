from nameparser import HumanName as hn
from csv import reader


if __name__ == '__main__':
    f = file('data/train.csv', 'r')
    lines = reader(f)

    # Write header
    atts = lines.next()

    for line in lines:
        name = hn(line[3])
        name_without_title = '%s %s %s' % (name.first, name.middle, name.last)

        print name
        print name_without_title
