from csv import reader
from decisiontree import Node, make_tree, write_tree
from initial_vis import make_variable_dictionary



if __name__ == '__main__':
    f = file('data/train_titles.csv', 'r')
    lines = reader(f)
    variables = lines.next()
    var_dict = make_variable_dictionary(variables)

    # Still only interested in Sex, Pclass, and Survived.
    index_sex = var_dict['Sex']
    index_pclass = var_dict['Pclass']
    index_title = var_dict['Title']
    index_age = var_dict['Age']
    index_survived = var_dict['Survived']

    # Gather (sex, pclass, survived) data from f
    data = []
    for line in lines:
        data.append([
            line[index_sex],
            int(line[index_pclass]),
            line[index_title],
            int(line[index_sibsp]),
            int(line[index_parch]),
            line[index_embarked]
    ])
    f.close()

    var_dict = {
        'Sex': 0,
        'Pclass': 1,
        'Title': 2,
        'SibSp': 3,
        'Parch': 4,
        'Embarked': 5
    }

    root = Node()
    ind_vars = {
        'Sex': [lambda x: x == val for val in ['male', 'female']],
        'Pclass': [lambda x: x == val for val in [1, 2, 3]],
        'Title': [
            lambda x: x == val for val in [
                'Mr', 'Master', 'Mrs', 'Miss', 'Rev', 'Dr', 'Col', '']],
        'SibSp': (
            [lambda x: x == val for val in [0, 1, 2, 3, 4]] +
            [lambda x: x>4]),
        'Parch': (
            [lambda x: x== val for val in [0, 1, 2]] + [lambda x: x>2]),
        'Embarked': [lambda x: x == val for val in ['S', 'C', 'Q']]
    }
    dep_vars = ['Survived', 0, 1]
    depth = 10
    root = make_tree(data, ind_vars, dep_vars, var_dict, depth)

    f = file('trees/discrete_survival.tree', 'w')
    write_tree(root, f)
    f.close()
