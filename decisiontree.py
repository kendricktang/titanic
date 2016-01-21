from math import log
import re


class Node(object):

    def __init__(self):
        self.variable = None
        self.distribution = None
        self.children = {}


    def predict(self, datum, var_dict):
        if not self.variable:
            return self.distribution

        split_val = datum[var_dict[self.variable]]
        return self.children[split_val].predict(datum, var_dict)


def calc_info_gain(old_entropy, N, data_subsets, dep_var, var_dict):
    # Sum up the information of the data_subsets, weighted by their
    # proportions.
    next_entropies = 0
    for subset in data_subsets.values():
        if subset:
            next_entropies += (
                calc_entropy(subset, dep_var, var_dict) * len(subset) / N
            )

    # Return the difference.
    return old_entropy - next_entropies


def calc_entropy(data, var_info, var_dict):
    distribution, singleton = calc_distribution(data, var_info, var_dict)
    counts = distribution.values()
    return sum(
        -count * log(count, 2) for count in counts if count
    )


def calc_distribution(data, dep_var, var_dict):
    """
    dep_var is of the form: ['name_of_var', val_0, val_1, ...] where val_i
    is a possible value that 'name_of_var' can take.
    This method returns a dictionary which maps each value to the probabilty
    that that value can occur.
    """
    n = len(data)
    var = dep_var[0]
    values = dep_var[1:]

    # Calculate distribution of dependent variable values
    distribution = {
        value: len([
            datum for datum in data if datum[var_dict[var]] == value])/float(n)
        for value in values}

    # Determine whether there is only one possible dependent variable value
    singleton = False
    for value in values:
        if distribution[value] > 0.99:
            singleton = True

    return distribution, singleton


def make_tree(data, ind_vars, dep_var, var_dict, remaining_depth):
    """
    Recursive method used to build a decision tree.

    dep_var is of the form: ['name_of_var', val_0, val_1, ...] where val_i
    is a possible value that 'name_of_var' can take.

    Note: if remaining_depth is set very large (e.g. 100), then this will
    recur until data is empty, which is one way to terminate a decision tree.
    """
    # Early return if depth is reached.
    if remaining_depth == 0:
        return None

    # Early return if there is no data.
    if not data:
        return None

    # Initialize variables
    node = Node()
    max_info_gain = None
    next_data = None
    next_variable = None

    node.distribution, singleton = calc_distribution(data, dep_var, var_dict)
    # If the decision has been made, don't bother with info_gain or children.
    if singleton:
        return node

    # Calculate entropy of current data
    entropy = calc_entropy(data, dep_var, var_dict)
    n = len(data)

    # Calculate the information gain for each independent variable
    for var in ind_vars.keys():
        values = ind_vars[var]
        data_subsets = {
            value: [
                datum for datum in data if datum[var_dict[var]] == value]
            for value in values}
        info_gain = calc_info_gain(entropy, n, data_subsets, dep_var, var_dict)
        if info_gain > max_info_gain:
            max_info_gain = info_gain
            next_data = data_subsets
            next_variable = var
            next_values = values

    # If there is no information gain, end here
    if max_info_gain == 0:
        return node

    # Using the independent variable with the most information gain,
    # recursively set this node's decision variable and its children.
    # If there's only one value left, then just stop here.
    if len([data_subset for data_subset in next_data.values() if data_subset]) < 2:
        print 'hello'
        return node
    node.variable = next_variable
    for value in next_values:
        node.children[value] = make_tree(
            next_data[value],
            ind_vars,
            dep_var,
            var_dict,
            remaining_depth - 1)

    return node

def write_tree(node, f):
    """
    Recursively write a tree.
    """
    for key in node.children.keys():
        if not node.children[key]:
            node.children.pop(key)

    f.write('%s,%s,%s\n' % (
            node.variable,
            str(node.distribution),
            str(node.children.keys()))
    )

    for child in node.children.values():
        write_tree(child, f)


def read_tree(filename):
    pat = re.compile('([^,]*),({[^{}]*}),(\[[^\[\]]*\])')
    f = file(filename, 'r')
    root = Node()

    line = f.next()
    data = pat.search(line)
    data = data.groups()

    # Set the root's variable and distribution
    root.variable = data[0]
    exec('root.distribution = %s' % data[1])

    # Recursively build children
    root.children = {}
    exec('children_keys = %s' % data[2])
    for key in children_keys:
        root.children[key] = read_tree_helper(f, pat)

    f.close()
    return root


def read_tree_helper(f, pat):
    try:
        line = f.next()
    except StopIteration:
        print "EOF"
        return

    node = Node()
    data = pat.search(line)
    data = data.groups()

    # Set the root's variable and distribution
    if data[0] == 'None':
        node.variable = None
    else:
        node.variable = data[0]
    exec('node.distribution = %s' % data[1])

    # Recursively build children
    node.children = {}
    exec('children_keys = %s' % data[2])
    for key in children_keys:
        node.children[key] = read_tree_helper(f, pat)
    return node
