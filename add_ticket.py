from csv import reader
import re
import sys


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError as e:
        print '%s: You need to input a file name.' % e
        raise

    f = file('data/%s.csv' % filename, 'r')
    f_out = file('data/%s_tickets.csv' % filename, 'w')
    lines = reader(f)

    # Set up regular expression 
    pattern_code = re.compile('([^\s]*)[\s]*')
    pattern_val = re.compile('[^0-9]*([0-9]+)')

    # Write header
    atts = lines.next()
    index_ticket = atts.index('Ticket')
    f_out.write(','.join(atts[0:index_ticket]))
    f_out.write(',Ticket_Code,Ticket_Val,')
    f_out.write(','.join(atts[index_ticket+1:]))
    f_out.write('\n')

    for line in lines:
        ticket = line[index_ticket]

        match_val = pattern_val.search(ticket)
        if not match_val:
            val = '0'
        else:
            val = match_val.group(1)

        match_code = pattern_code.search(ticket)
        code = match_code.group(1)
        if code == val:
            code = ''

        # Write data, with added title and name section.
        f_out.write(','.join(line[0:index_ticket]))
        f_out.write(',%s,%s,' % (code, val))
        f_out.write(','.join(line[index_ticket+1:]))
        f_out.write('\n')
