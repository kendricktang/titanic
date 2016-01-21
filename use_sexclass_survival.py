from csv import reader
from decisiontree import read_tree
from initial_vis import make_variable_dictionary

if __name__ == '__main__':
    tree = read_tree('trees/sexclass_survival.tree')

    f = file('data/test.csv', 'r')
    lines = reader(f)
    variables = lines.next()
    var_dict = make_variable_dictionary(variables)

    # Still only interested in Sex, Pclass, and Survived.
    index_passengerId = var_dict['PassengerId']
    index_sex = var_dict['Sex']
    index_pclass = var_dict['Pclass']

    # Gather (sex, pclass, survived) data from f
    data = []
    for line in lines:
        data.append([int(line[index_passengerId]),
                     line[index_sex],
                     int(line[index_pclass])])
    f.close()
    var_dict = {'PassengerId': 0, 'Sex': 1, 'Pclass': 2}  # Simplified var_dict.

    f = file('predictions/sexclass_survival.csv', 'w')
    f.write('PassengerId,Survived\n')
    for datum in data:
        distribution = tree.predict(datum, var_dict)
        if distribution[0] < distribution[1]:
            f.write('%d,%d\n' % (datum[var_dict['PassengerId']], 1))
        else:
            f.write('%d,%d\n' % (datum[var_dict['PassengerId']], 0))
