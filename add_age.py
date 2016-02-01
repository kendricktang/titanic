from csv import reader
import sys
from titles import titles
from ticket_codes import ticket_codes
from make_titanic_tree import construct, simplify_var_dict
from use_titanic_tree import get_data, write_prediction
from decisiontree import read_tree, write_tree

def separate_age(filename):
    """
    Given a filename in the data folder, the data is split into two files:
    one containing data entries which have valid age values, and
    one containing data entries which doen't have valid  age values.
    """
    f_original = file('data/%s.csv' % filename, 'r')
    f_no_age = file('data/%s_no_age.csv' % filename, 'w')
    f_age = file('data/%s_age.csv' % filename, 'w')

    lines = reader(f_original)
    atts = lines.next()
    index_age = atts.index('Age')
    f_no_age.write(','.join(atts[0:index_age]))
    f_no_age.write(',')
    f_no_age.write(','.join(atts[index_age+1:]))
    f_no_age.write('\n')
    f_age.write(','.join(atts))
    f_age.write('\n')

    for line in lines:
        age = line[index_age]
        if age:
            f_age.write(','.join(line))
            f_age.write('\n')
        else:
            f_no_age.write(','.join(line[0:index_age]))
            f_no_age.write(',')
            f_no_age.write(','.join(line[index_age+1:]))
            f_no_age.write('\n')
    f_original.close()
    f_no_age.close()
    f_age.close()


def write_age_file(filename):
    """
    Given the filename of a data file, the predicted ages from ages.csv 
    are added to the the data and a new data file is written.
    """
    f_original = file('data/%s.csv' % filename, 'r')
    f_age = file('predictions/ages.csv', 'r')
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


if __name__ =='__main__':
    try:
        filename = sys.argv[1]
    except IndexError as e:
        print '%s: You need to input a file name.' % e
        raise

    try:
        build_tree = sys.argv[2]
        print "building a new tree"
    except:
        print "using a pre-built tree"
        build_tree = None

    separate_age(filename)
    ind_vars = {
        ('Sex', 'categorical'): ['male', 'female'],
        ('Pclass', 'categorical'): ['1', '2', '3'],
        ('Embarked', 'categorical'): ['S', 'C', 'Q'],
        ('SibSp', 'continuous'): None,
        ('Parch', 'continuous'): None,
        ('Fare', 'continuous'): None,
        # ('Title', 'categorical'): titles,
        # ('Ticket_Code', 'categorical'): ticket_codes,
        # ('Ticket_Val', 'continuous'): None,
    }
    target_var = ['Age', 'continuous']

    # Only build a tree if necessary.
    if build_tree:
        # Build tree to predict age:
        f = file('data/%s_age.csv' % filename, 'r')
        max_depth = 6
        root = construct(f, ind_vars, target_var, max_depth)
        f.close()

        f = file('trees/age.tree', 'w')
        write_tree(root, f)
        f.close()

        # Trim tree: TODO

    # Use tree to predict age:
    # Compile list of independent variables used to predict target variable
    tree = read_tree('trees/age.tree')
    f = file('data/%s_no_age.csv' % filename, 'r')
    ind_vars[('PassengerId', 'continuous')] = None
    data = get_data(f, ind_vars)
    var_dict = simplify_var_dict(ind_vars, None)

    # Output target variable predictions to csv.
    f = file('predictions/ages.csv', 'w')
    f.write('PassengerId,%s\n' % target_var[0])
    for datum in data:
        distribution = tree.predict(datum, var_dict)
        write_prediction(
                f,
                distribution,
                target_var,
                int(datum[var_dict['PassengerId']]))
    f.close()

    # Write a new data file with age values.
    write_age_file(filename)
