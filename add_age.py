from csv import reader
import sys


if __name__ =='__main__':
    try:
        filename = sys.argv[1]
    except IndexError as e:
        print e

    f_original = file('data/%s.csv' % filename, 'r')
    f_age = file('predictions/test_simple_age.csv', 'r')
    f_new = file('data/%s_ages.csv' % filename, 'w')

    data_age = {}
    lines = reader(f_age)
    atts_age = lines.next()
    for line in lines:
        id = line[0]
        age = line[1]
        data_age[id] = age
    f_age.close()

    lines = reader(f_original)
    atts = lines.next()
    index_age = atts.index('Age')
    index_id = atts.index('PassengerId')
    f_new.write('%s\n' % ','.join(atts))

    for line in lines:
        age = line[index_age]
        id = line[index_id]
        if not age:
            age = data_age[id]
            line[index_age] = age
        f_new.write('%s\n' % ','.join(line))

    f_original.close()
    f_new.close()
