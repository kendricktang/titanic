from csv import reader
from decisiontree import Node, make_tree, write_tree
from initial_vis import make_variable_dictionary



if __name__ == '__main__':
    f = file('data/train.csv', 'r')
    lines = reader(f)
    variables = lines.next()
    var_dict = make_variable_dictionary(variables)

    # Still only interested in Sex, Pclass, and Survived.
    index_sex = var_dict['Sex']
    index_pclass = var_dict['Pclass']
    index_survived = var_dict['Survived']

    # Gather (sex, pclass, survived) data from f
    data = []
    for line in lines:
        data.append([line[index_sex],
                     int(line[index_pclass]),
                     int(line[index_survived])])
    f.close()
    var_dict = {'Sex': 0, 'Pclass': 1, 'Survived': 2}  # Simplified var_dict.

    root = Node()
    ind_vars = {
        'Sex': ['male', 'female'],
        'Pclass': [1, 2, 3]
    }
    dep_vars = ['Survived', 0, 1]
    depth = 10
    root = make_tree(data, ind_vars, dep_vars, var_dict, depth)

    f = file('trees/sexclass_survival_test.tree', 'w')
    write_tree(root, f)
    f.close()
