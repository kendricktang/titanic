from matplotlib import pyplot as plt
import numpy as np
from csv import reader

def plot_bar_set(dataset, subplot, keys=None):
    """
    Given a data dictionary, where each key points to survival data,
    each set of survival data is plotted.

    Keys can be reordered to make more spacial sense.

    subplot must be defined before hand:
        Subplot is a three digit integer used to define the rows/columns of
        subplots. This value is incremented.
    """
    if not keys:
        keys = dataset.keys()

    for key in keys:
        # Set x-axis properties
        ax = plt.subplot(subplot)
        ticks = np.array((0.125, 0.625))
        width = 0.25
        ticklabels = ('died', 'survived')
        ax.set_xlim(0, 1)
        ax.set_xticks(ticks + width/2)
        ax.set_xticklabels(ticklabels, size='large')

        # Set title
        ax.set_title(str(key))

        ax.bar(ticks, dataset[key], width)
        subplot += 1

def make_variable_dictionary(variables):
    """
    Given an array of variables, returns a dictionary that maps
    the name of an variable to its index.
    """
    var_dict = {}
    for index in range(len(variables)):
        var_dict[variables[index]] = index
    return var_dict


def add_to_data(data, key, survived):
    """
    Adds the datum (key, survived) to the dictionary data,
    and accounts for when key is not in data.keys().
    """
    if key not in data.keys():
        data[key] = [0, 0]
    data[key][survived] += 1



def read_csv(filename):
    """
    Reads filename and creates three data dictionaries.
    One for the surival based on sex, one for survival based on pclass,
    and one based on (sex, pclass) 2-tuples.
    """
    f = file(filename, 'r')
    lines = reader(f)
    variables = lines.next()

    var_dict = make_variable_dictionary(variables)

    # I'm only interested in Pclass, Sex, and Survived.
    paired_data = {}
    sex_data = {}
    pclass_data = {}
    for line in lines:
        # Get sex, pclass, and survived for each passenger
        sex = line[var_dict['Sex']]
        pclass = int(line[var_dict['Pclass']])
        survived = int(line[var_dict['Survived']])

        add_to_data(paired_data, (sex, pclass), survived)
        add_to_data(sex_data, sex, survived)
        add_to_data(pclass_data, pclass, survived)
    f.close()
    return paired_data, sex_data, pclass_data


if __name__ == '__main__':
    paired_data, sex_data, pclass_data = read_csv('data/train.csv')

    # Plot paired data (3x2 plot)
    plt.figure(1)
    plt.subplots_adjust(hspace=0.4)
    subplot = 321

    # Use Python's stable sort to organize the subplots.
    keys = sorted(paired_data.keys(), key=lambda x: x[0], reverse=True)
    keys = sorted(keys, key=lambda x: x[1])

    plot_bar_set(paired_data, subplot, keys=keys)
    plt.savefig('plots/paired')
    plt.clf()
    plt.close()

    # Plot sex data (2x1 plot)
    plt.figure(2)
    subplot = 121
    plot_bar_set(sex_data, subplot)
    plt.savefig('plots/sex')
    plt.clf()
    plt.close()

    # Plot pclass data (3x1 plot)
    plt.figure(3)
    plt.subplots_adjust(wspace=0.3)
    subplot = 131
    plot_bar_set(pclass_data, subplot)
    plt.savefig('plots/pclass')
    plt.clf()
    plt.close()
