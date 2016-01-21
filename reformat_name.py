from nameparser import HumanName
from csv import reader
import string
import sys

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError as e:
        print '%s: You need to input a file name.' % e
        raise
 
    f = file('data/%s.csv' % filename, 'r')
    f_out = file('data/%s_titles.csv' % filename, 'w')
    lines = reader(f)

    # Write header
    atts = lines.next()
    index_name = atts.index('Name')
    f_out.write(','.join(atts[0:index_name]))
    f_out.write(',Title,Name,')
    f_out.write(','.join(atts[index_name+1:]))
    f_out.write('\n')

    for line in lines:
        name = HumanName(line[index_name])

        # Simply titles.
        title = str(name.title)
        title = title.translate(string.maketrans('', ''), string.punctuation)
        if title == 'Ms':
            title = 'Miss'
        if title == 'Lady':
            title = 'Mrs'
        if title == 'Sir':
            title = 'Mr'
        if title == 'Capt':
            title = 'Col'

        # Simplify names. Some names will have improper formatting, but I don't
        # plan on using names to build decision trees, yet.
        if name.middle:
            name_without_title = '%s %s %s' % (
                name.first, name.middle, name.last)
        else:
            name_without_title = '%s %s' % (name.first, name.last)

        # Write data, with added title and name section.
        f_out.write(','.join(line[0:index_name]))
        f_out.write(',%s,%s,' % (title, name_without_title))
        f_out.write(','.join(line[index_name+1:]))
        f_out.write('\n')
