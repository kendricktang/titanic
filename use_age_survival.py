from csv import reader
from decisiontree import read_tree
from initial_vis import make_variable_dictionary

if __name__ == '__main__':
    tree = read_tree('trees/age_survival.tree')

    f = file('data/test_titles_ages.csv', 'r')
    lines = reader(f)
    variables = lines.next()
    var_dict = make_variable_dictionary(variables)

    # Still only interested in Sex, Pclass, and Survived.
    index_passengerId = var_dict['PassengerId']
    index_sex = var_dict['Sex']
    index_pclass = var_dict['Pclass']
    index_title = var_dict['Title']
    index_sibsp = var_dict['SibSp']
    index_parch = var_dict['Parch']
    index_embarked = var_dict['Embarked']

    # Gather (sex, pclass, survived) data from f
    data = []
    for line in lines:
        data.append([
            int(line[index_passengerId]),
            line[index_sex],
            int(line[index_pclass]),
            line[index_title],
            int(line[index_sibsp]),
            int(line[index_parch]),
            line[index_embarked]
        ])
    f.close()

    var_dict = {
        'PassengerId': 0,
        'Sex': 1,
        'Pclass': 2,
        'Title': 3,
        'SibSp': 4,
        'Parch': 5,
        'Embarked': 6
    }

    f = file('predictions/age_survival.csv', 'w')
    f.write('PassengerId,Survived\n')
    for datum in data:
        distribution = tree.predict(datum, var_dict)
        if distribution[0] < distribution[1]:
            f.write('%d,%d\n' % (datum[var_dict['PassengerId']], 1))
        else:
            f.write('%d,%d\n' % (datum[var_dict['PassengerId']], 0))
