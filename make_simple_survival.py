from csv import reader
from decisiontree import make_tree, write_tree
from initial_vis import make_variable_dictionary


if __name__ == '__main__':
    f = file('data/train_titles.csv', 'r')
    lines = reader(f)
    variables = lines.next()
    var_dict = make_variable_dictionary(variables)

    index_sex = var_dict['Sex']
    index_pclass = var_dict['Pclass']
    index_title = var_dict['Title']
    index_sibsp = var_dict['SibSp']
    index_parch = var_dict['Parch']
    index_embarked = var_dict['Embarked']
    index_survived = var_dict['Survived']

    # Gather data from file, only keeping relevant information
    data = []
    for line in lines:
        data.append([
            line[index_sex],
            int(line[index_pclass]),
            line[index_title],
            int(line[index_sibsp]),
            int(line[index_parch]),
            line[index_embarked],
            int(line[index_survived])
        ])
    f.close()

    var_dict = {
        'Sex': 0,
        'Pclass': 1,
        'Title': 2,
        'SibSp': 3,
        'Parch': 4,
        'Embarked': 5,
        'Survived': 6
    }

    ind_vars = {
        ('Sex', 'discrete'): ['male', 'female'],
        ('Pclass', 'discrete'): [1, 2, 3],
        ('Title', 'discrete'): [
            'Mr', 'Master', 'Mrs', 'Miss', 'Rev', 'Dr', 'Col', ''],
        ('SibSp', 'continuous'): None,
        ('Parch', 'continuous'): None,
        ('Embarked', 'discrete'): ['S', 'C', 'Q']
    }
    dep_vars = ['Survived', 0, 1]
    depth = 4
    root = make_tree(data, ind_vars, dep_vars, var_dict, depth)

    f = file('trees/discrete_survival.tree', 'w')
    write_tree(root, f)
    f.close()
