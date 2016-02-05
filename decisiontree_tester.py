import numpy as np
from matplotlib import pyplot as plt
from make_titanic_tree import construct, simplify_var_dict, write_tree
from use_titanic_tree import get_data, write_prediction
from ticket_codes import ticket_codes
from titles import titles


def partition_data(filename, train_size, test_size, replacement):
    """
    Partitions the available data (at filename) into a training set
    and a testing set. If there replacement, then bootstrapping is used.
    Otherwise, a simple shuffle and partition is used.

    The training and testing set are written to my_train.csv and my_test.csv,
    respectively.
    """
    f_original = file('data/%s.csv' % filename, 'r')
    f_train = file('data/my_train.csv', 'w')
    f_test = file('data/my_test.csv', 'w')

    atts = f_original.next()
    lines = []
    for line in f_original:
        lines.append(line)
    f_original.close()
    lines = np.array(lines)

    # Use shuffle and partition sampling
    if not replacement:
        N = len(lines)
        if train_size + test_size > N:
            raise Exception(
                    ('Train and test sizes are too large.' +
                    'Train: %d, Test: %d, N: %d' % (train_size, test_size, N)))
        ind = range(N)
        np.random.shuffle(ind)
        train_ind = ind[:train_size]
        test_ind = ind[train_size: train_size+test_size]

    # Use bootstrap sampling
    else:
        train_ind = np.random.randint(0, len(lines), train_size)
        test_ind = np.random.randint(0, len(lines), test_size)

    # Sample train and test data
    train = lines[train_ind]
    test = lines[test_ind]

    # Write train and test data
    f_train.write(atts)
    for line in train:
        f_train.write(line)
    f_train.close()

    f_test.write(atts)
    for line in test:
        f_test.write(line)
    f_test.close()


def write_predictions(filename, ind_vars, tree):
    """
    Given data from data/filename.csv, the predicted target value
    for each passenger ID is written to predictions/filename.csv.
    """
    # Get the data set for prediction.
    f = file('data/%s.csv' % filename, 'r')
    data = get_data(f, ind_vars)
    var_dict = simplify_var_dict(ind_vars, None)
    f.close()

    # Output target variable predictions to csv.
    f = file('predictions/%s.csv' % filename, 'w')
    f.write('PassengerId,%s\n' % target_var[0])
    for datum in data:
        distribution = tree.predict(datum, var_dict)
        write_prediction(
                f,
                distribution,
                target_var,
                int(datum[var_dict['PassengerId']]))
    f.close()


def calc_performance(filename, target_var):
    """
    Calculates SSE of predictions of the target_variable.
    Note: actual values must be at data/filename.csv, and
    predicted values must be at predictions/filename.csv.
    """
    variables = {('PassengerId', 'continuous'): None}
    variables[(target_var[0], target_var[1])] = target_var[2:]

    var_dict = simplify_var_dict(variables, None)
    targ_var_name = target_var[0]
    targ_var_type = target_var[1]

    # Get actual values
    f = file('data/%s.csv' % filename, 'r')
    data = get_data(f, variables)
    f.close()

    # Get predicted values
    f = file('predictions/%s.csv' % filename, 'r')
    predictions = get_data(f, variables)
    f.close()

    if targ_var_type == 'categorical':
        wrong = 0
        for ind in xrange(len(data)):
            a = data[ind][var_dict[target_var[0]]]
            b = predictions[ind][var_dict[target_var[0]]]
            if a != b:
                wrong += 1
        return wrong
    elif targ_var_type == 'continuous':
        SSE = 0
        for ind in xrange(len(data)):
            actual_value = data[ind][var_dict[targ_var_name]]
            predicted_value = predictions[ind][var_dict[targ_var_name]]
            SSE += (actual_value - predicted_value)**2
        return SSE


def eval_tree_once(filename, train_size, test_size, replacement,
        ind_vars, target_var, max_depth):
    """
    Evaluates a tree by sampling the training and testing data sets once.

    Returns the error for cross validation (SSE with respect to test set)
    and the error for evaluating residuals (SSE with respect to train set)
    """

    partition_data(filename, train_size, test_size, replacement)

    # Build tree from train data
    f = file('data/my_train.csv', 'r')
    tree = construct(f, ind_vars, target_var, max_depth)
    f.close()

    # Write tree, just to see what the tree looks like.
    f = file('trees/my_tree.tree', 'w')
    write_tree(tree, f)
    f.close()

    # Append PassengerId as a variable for prediction purposes.
    ind_vars[('PassengerId', 'continuous')] = None

    # Make predictions on both test and train data sets.
    write_predictions('my_test', ind_vars, tree)
    write_predictions('my_train', ind_vars, tree)

    # Remove PassengerId from ind_vars
    ind_vars.pop(('PassengerId', 'continuous'), None)

    # calculate errors for both test and train data sets
    cross_val_error = calc_performance('my_test', target_var)
    res_error = calc_performance('my_train', target_var)

    return cross_val_error, res_error


def eval_tree(trials, filename, train_size, test_size, replacement,
        ind_vars, target_var, max_depth):
    """
    Evaluates a tree by sampling the training and testing data sets
    multiple times.

    Returns the errors for cross validation (SSE with respect to test set)
    and the errors for evaluating residuals (SSE with respect to train set)
    """

    cross_val_error = []
    residual_error = []
    for trial in xrange(trials):
        cross_val_err, residual_err = eval_tree_once(
                filename, train_size, test_size, replacement,
                ind_vars, target_var, max_depth)
        cross_val_error.append(cross_val_err)
        residual_error.append(residual_err)
    return np.array(cross_val_error), np.array(residual_error)


if __name__ == '__main__':
    filename = 'train_titles_tickets'
    train_size = 600
    test_size = 290
    replacement = False

    ind_vars = {
        ('Sex', 'categorical'): ['male', 'female'],
        ('Pclass', 'categorical'): ['1', '2', '3'],
        ('Embarked', 'categorical'): ['S', 'C', 'Q'],
        ('Title', 'categorical'): titles,
        ('Ticket_Code', 'categorical'): ticket_codes
    }
    target_var = ['Survived', 'categorical', '0', '1']
    max_depth = 100
    trials = 500

    cross_val_error, residual_error = eval_tree(
                trials, filename, train_size, test_size, replacement,
                ind_vars, target_var, max_depth)

    print 'Cross Validation errors: %f, %f' % (
        cross_val_error.mean() / test_size,
        cross_val_error.std() / test_size
    )
    print 'Residual errors: %f, %f' % (
        residual_error.mean() / train_size,
        residual_error.std() / train_size
    )

    plt.figure()
    plt.subplot(121)
    plt.hist(cross_val_error / float(test_size), color='#f46151')
    plt.xlabel('Cross Validation Error Distribution', size='large')
    plt.xticks(size=8)
    plt.yticks(size=8)
    plt.title('mu=%1.3f, std=%1.3f' % (cross_val_error.mean() / test_size, cross_val_error.std() / test_size), size='large')

    plt.subplot(122)
    plt.hist(residual_error / float(train_size), color='#f46151')
    plt.xlabel('Residual Error Distribution', size='large')
    plt.xticks(size=8)
    plt.yticks(size=8)
    plt.title('mu=%1.3f, std=%1.3f' % (residual_error.mean() / train_size, residual_error.std() / train_size), size='large')

    plt.suptitle('Sex, PClass, Embarked, Titles, Ticket Codes, and Mean Squared Error (MSE)', size='large')
    plt.savefig('plots/error_sex_pclass_embarked_titles_ticketcodes')
    plt.clf()
