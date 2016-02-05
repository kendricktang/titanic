from csv import reader
from decisiontree import make_tree, write_tree
from initial_vis import make_variable_dictionary
from ticket_codes import ticket_codes
from titles import titles


def construct(f, ind_vars, target_var, max_depth):
    """
    Given a csv data file 'f', a list of independent variables, and the target
    variable, a tree is built and returned.
    """
    lines = reader(f)
    variables = lines.next()
    var_dict = make_variable_dictionary(variables)

    # Collect all of the data, but only the variables of interest.
    data = []
    for line in lines:
        datum = get_datum(line, var_dict, ind_vars, target_var)
        data.append(datum)

    # Simplify variable dictionary:
    var_dict = simplify_var_dict(ind_vars, target_var)

    return make_tree(data, ind_vars, target_var, var_dict, max_depth, len(data))


def simplify_var_dict(ind_vars, target_var):
    """
    Simplifies the variable dictionary to only include the independent
    variables of interest, and the target variable. Also makes the variable
    dictionary match the structure of the data being used to build the tree.
    """
    var_dict = {}
    index = 0
    for ind_var in ind_vars.keys():
        var_dict[ind_var[0]] = index
        index += 1

    if target_var:
        var_dict[target_var[0]] = index

    return var_dict


def get_datum(line, var_dict, ind_vars, target_var):
    datum = []
    # Append independent variables
    for var in ind_vars.keys():
        if var[1] == 'categorical':
            datum.append(line[var_dict[var[0]]])
        elif var[1] == 'continuous':
            datum.append(float(line[var_dict[var[0]]]))
        else:
            raise Exception('Invalid variable type: %s' % var[1])

    # Append target variable
    if target_var and target_var[1] == 'categorical':
        datum.append(line[var_dict[target_var[0]]])
        pass
    elif target_var and target_var[1] == 'continuous':
        datum.append(float(line[var_dict[target_var[0]]]))
    elif target_var:
        raise Exception('Invalid variable type: %s' % target_var[1])

    return datum


if __name__ == '__main__':
    f = file('data/train_titles.csv', 'r')
    ind_vars = {
        ('Sex', 'categorical'): ['male', 'female'],
        ('Pclass', 'categorical'): ['1', '2', '3'],
        ('Embarked', 'categorical'): ['S', 'C', 'Q'],
        ('Title', 'categorical'): titles,
        ('Ticket_Code', 'categorical'): ticket_codes,
        ('SibSp', 'continuous'): None,
        ('Parch', 'continuous'): None,
        ('Fare', 'continuous'): None,
        ('Ticket_Val', 'continuous'): None,
    }
    target_var = ['Survived', 'categorical', '0', '1']
    max_depth = 100
    tree = construct(f, ind_vars, target_var, max_depth)
    f.close()

    f = file('trees/temp.tree', 'w')
    write_tree(tree, f)
    f.close()
