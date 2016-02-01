from csv import reader
from decisiontree import read_tree
from initial_vis import make_variable_dictionary
from make_titanic_tree import get_datum, simplify_var_dict
from ticket_codes import ticket_codes
from titles import titles


def get_data(f, ind_vars):
    """
    Reads f and returns a list of the independent variables.
    """
    lines = reader(f)
    variables = lines.next()
    var_dict = make_variable_dictionary(variables)

    # Collect all of the data, but only the variables of interest.
    data = []
    for line in lines:
        datum = get_datum(line, var_dict, ind_vars, None)
        data.append(datum)
    return data


def write_prediction(f, distribution, target_var, key):
    """
    Writes the predicted value of the target variable.
    """
    f.write(str(key))
    if target_var[1] == 'categorical':
        max_val = 0
        max_key = None
        for key in distribution.keys():
            val = distribution[key]
            if val > max_val:
                max_val = val
                max_key = key
        f.write(',%s\n' % max_key)
    elif target_var[1] == 'continuous':
        f.write(',%f\n' % distribution[0])
    else:
        raise Exception('Invalid varaible type: %s' % target_var[1])


if __name__ == '__main__':
    # Build tree from a .tree file.
    tree = read_tree('trees/cat_cont_with_age.tree')

    # Compile list of independent variables used to predict target variable
    f = file('data/test_titles_tickets_ages.csv', 'r')
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
        ('PassengerId', 'continuous'): None,
    }
    target_var = ['Survived', 'categorical', '0', '1']
    data = get_data(f, ind_vars)
    var_dict = simplify_var_dict(ind_vars, None)

    # Output target variable predictions to csv.
    f = file('predictions/cat_cont_with_age.csv', 'w')
    f.write('PassengerId,%s\n' % target_var[0])
    for datum in data:
        distribution = tree.predict(datum, var_dict)
        write_prediction(
                f,
                distribution,
                target_var,
                int(datum[var_dict['PassengerId']]))
    f.close()
