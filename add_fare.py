from csv import reader
import sys
import os


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError as e:
        print '%s: You need to input a file name.' % e
        raise

    f = file('data/%s.csv' % filename, 'r')
    f_out = file('data/%s_temp.csv' % filename, 'w')
    lines = reader(f)


    # Write header
    atts = lines.next()
    index_fare = atts.index('Fare')
    f_out.write(','.join(atts))
    f_out.write('\n')

    for line in lines:
        fare = line[index_fare]
        if not fare:
            fare = '0'

        # Write data, with added title and name section.
        f_out.write(','.join(line[0:index_fare]))
        f_out.write(',%s,' % fare)
        f_out.write(','.join(line[index_fare+1:]))
        f_out.write('\n')

    # Rename the temp file to override the original file.
    os.rename('data/%s_temp.csv' % filename, 'data/%s.csv' % filename)
