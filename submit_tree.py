from make_titanic_tree import construct, simplify_var_dict, write_tree
from use_titanic_tree import get_data, write_prediction
from ticket_codes import ticket_codes
from titles import titles


if __name__ == '__main__':
    filename_train = 'train_titles_tickets'
    filename_tree = 'submission'
    filename_test = 'test_titles_tickets'
    filename_predictions = 'submission'

    # Which variables do you want to use? What is the target variable?
    ind_vars = {
        ('Sex', 'categorical'): ['male', 'female'],
        ('Pclass', 'categorical'): ['1', '2', '3'],
        ('Embarked', 'categorical'): ['C', 'S', 'Q'],
        ('Title', 'categorical'): titles,
        ('Ticket_Code', 'categorical'): ticket_codes,
    }
    target_var = ['Survived', 'categorical', '0', '1']
    max_depth = 100

    # Build tree!
    f = file('data/%s.csv' % filename_train, 'r')
    tree = construct(f, ind_vars, target_var, max_depth)
    f.close()

    # Write tree to file. Not necessary, but nice to have.
    f = file('trees/%s.tree' % filename_tree, 'w')
    write_tree(tree, f)
    f.close()

    # Append PassengerId for prediction purposes.
    f = file('data/%s.csv' % filename_test, 'r')
    ind_vars[('PassengerId', 'continuous')] = None
    data = get_data(f, ind_vars)
    var_dict = simplify_var_dict(ind_vars, None)
    f.close()

    # Output target variable predictions to csv.
    f = file('predictions/%s.csv' % filename_predictions, 'w')
    f.write('PassengerId,%s\n' % target_var[0])
    for datum in data:
        distribution = tree.predict(datum, var_dict)
        write_prediction(
                f,
                distribution,
                target_var,
                int(datum[var_dict['PassengerId']]))
    f.close()
