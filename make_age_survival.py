from csv import reader
from decisiontree import make_tree, write_tree
from initial_vis import make_variable_dictionary


if __name__ == '__main__':
    f = file('data/train_ages.csv', 'r')
    lines = reader(f)
    variables = lines.next()
    var_dict = make_variable_dictionary(variables)

    index_sex = var_dict['Sex']
    index_pclass = var_dict['Pclass']
    index_title = var_dict['Title']
    index_age = var_dict['Age']
    index_sibsp = var_dict['SibSp']
    index_parch = var_dict['Parch']
    index_embarked = var_dict['Embarked']
    index_survived = var_dict['Survived']

    data = []
    for line in lines:
        data.append([
            line[index_sex],
            int(line[index_pclass]),
            line[index_title],
            float(line[index_age]),
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
        'Age': 3,
        'SibSp': 4,
        'Parch': 5,
        'Embarked': 6,
        'Survived': 7
    }

    ind_vars = {
        ('Sex', 'discrete'): ['male', 'female'],
        ('Pclass', 'discrete'): [1, 2, 3],
        ('Title', 'discrete'): [
            'Mr', 'Master', 'Mrs', 'Miss', 'Rev', 'Dr', 'Col', ''],
        ('Age', 'continuous'): None,
        ('SibSp', 'continuous'): None,
        ('Parch', 'continuous'): None,
        ('Embarked', 'discrete'): ['S', 'C', 'Q']
    }
    dep_vars = ['Survived', 'discrete', 0, 1]
    depth = 10
    root = make_tree(data, ind_vars, dep_vars, var_dict, depth, len(data))

    f = file('trees/age_survival.tree', 'w')
    write_tree(root, f)
    f.close()
