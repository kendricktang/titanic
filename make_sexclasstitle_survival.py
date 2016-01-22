from csv import reader
from decisiontree import make_tree, write_tree
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
        data.append([line[index_sex],
                     int(line[index_pclass]),
                     line[index_title],
                     int(line[index_survived]),
                     line[index_age]])
    f.close()
    var_dict = {'Sex': 0, 'Pclass': 1, 'Title': 2, 'Survived': 3, 'Age': 4}

    ind_vars = {
        ('Sex', 'discrete'): ['male', 'female'],
        ('Pclass', 'discrete'): [1, 2, 3],
        ('Title', 'discrete'): [
            'Mr', 'Master', 'Mrs', 'Miss', 'Rev', 'Dr', 'Col', '']
    }
    dep_vars = ['Survived', 'discrete', 0, 1]
    depth = 10
    root = make_tree(data, ind_vars, dep_vars, var_dict, depth)

    f = file('trees/sexclasstitle_survival_test.tree', 'w')
    write_tree(root, f)
    f.close()
