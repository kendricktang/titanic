from math import log
import re
import numpy as np


class Node(object):
    """
    A Node object used for decision trees.
    Three fields:
        variable:
            valid formats are ('varname', 'categorical') or
            ('varname', 'continuous', splitval).
            This field contains information about what variable this tree
            uses to make a decision, and how it makes it.

        distribution:
            if target variable is categorical, this is a dictionary which
            maps target values to their probability.
            if target variable is continuous, this is a 2-tuple (mu, SSE).

        children:
            if variable is categorical, this is a dictionary which maps
            variable values to their nodes.
            if variable is continuous, this is a dictionary which has two
            keys: less, and more. They point to the nodes corresponding
            to when the variable value is less than the splitval,
            and when the variable value is more than the splitval.
    """

    def __init__(self):
        # Valid format for self.variable is:
        # ('varname', 'categorical')
        # ('varname', 'continuous', splitval)
        self.variable = None

        self.distribution = None
        self.children = {}

    def predict(self, datum, var_dict):
        """
        Given a data point, the tree is walked until a decision is made,
        and the distribution of the last node is returned.

        Note: the recursion may end before arriving at a leaf node.
        """
        if not self.variable:
            return self.distribution

        var_val = datum[var_dict[self.variable[0]]]
        var_type = self.variable[1]
        if var_type == 'categorical':
            try:
                return self.children[var_val].predict(datum, var_dict)
            except KeyError:
                # print 'Warning: decision was made early (i.e. not at leaf)'
                return self.distribution
        elif var_type == 'continuous':
            if var_val < self.variable[2]:
                try:
                    return self.children['less'].predict(datum, var_dict)
                except AttributeError:
                    print 'Warning: decision was made early (i.e. not at leaf)'
                    return self.distribution
            else:
                try:
                    return self.children['more'].predict(datum, var_dict)
                except AttributeError:
                    print 'Warning: decision was made early (i.e. not at leaf)'
                    return self.distribution
        else:
            raise Exception('Invalid variable type: %s' % self.variable[2])

    def __str__(self):
        return '%s,%s,%s' % (
                self.variable,
                str(self.distribution),
                str(self.children.keys()))


def calc_entropy(data, var_info, var_dict):
    """
    Assumes target variable is a categorical type. Returns the entropy of
    the data with respect to the categorical target variable.
    """
    var = var_info[0]
    var_values = var_info[2:]
    distribution = {}
    N = len(data)
    for value in var_values:
        distribution[value] = (
            len(
                [datum for datum in data if datum[var_dict[var]] == value]
            ) / float(N)
        )

    counts = distribution.values()
    return sum(
        -count * log(count, 2) for count in counts if count
    )


def calc_distribution(data, targ_var, var_dict):
    """
    If the target variable is categorical, this method returns a dictionary
    which maps each value that the dependent variable can take to the
    probabilty that the value can occur.

    If the target variable is continuous, this method returns a 2-tuple which
    contains the (mean, variance) of the target variable.
    """
    var = targ_var[0]
    targ_var_type = targ_var[1]
    N = len(data)
    if N == 0:
        return 0

    if targ_var_type == 'categorical':
        targ_var_values = targ_var[2:]
        distribution = {}
        for value in targ_var_values:
            distribution[value] = (
                len(
                    [datum for datum in data if datum[var_dict[var]] == value]
                ) / float(N)
            )
        return distribution

    elif targ_var_type == 'continuous':
        targ_var_data = np.array([datum[var_dict[var]] for datum in data])
        return (targ_var_data.mean(), targ_var_data.var())

    else:
        raise Exception('Invalid variable type: %s' % targ_var_type)


def early_termination_pre(data, remaining_depth):
    """
    Early termination check before looking at splits
    """
    if remaining_depth == 0:
        return True

    if not data:
        return True

    return False


def early_termination_post(next_data):
    """
    Early termination check after looking at splits
    """

    if not next_data:
        return True

    if len(
            [data_subset for data_subset in next_data.values()
                if data_subset]) < 2:
        return True
    return False


def check_singleton(distribution):
    """
    Returns true if there is only one real value left in the distribution
    (with respect to epsilon). Otherwise, returns false.
    """
    epsilon = 0.01

    if type(distribution) == tuple:  # continuous target variable
        variance = distribution[1]
        if variance < epsilon:
            return True
    elif type(distribution) == dict:  # categorical target variable
        for value in distribution.values():
            if value > 1 - epsilon:
                return True
    else:
        raise Exception('Invalid distribution: %s' % str(distribution))

    return False


def partition_data(data, var, var_type, var_vals, var_dict):
    """
    If variable type is categorical, then data is partitioned by variable
    values and a single partition is returned.

    If variable type is continuous, then for each variable value, data is
    partitioned into two subsets, and the set of partitions is returned.
    """
    subsets = {}
    if var_type == 'categorical':
        # Simply partition by the categorical variable. Keys in subset are
        # values and they map to a single subset.
        for value in var_vals:
            subsets[value] = [
                datum for datum in data if datum[var_dict[var]] == value]
    elif var_type == 'continuous':
        # For each variable value, partition into a less-than and a
        # greater-than set. Keys in subset are values and they map to a
        # partition of data. This is much bigger than for categorical
        # variables.

        # Get values:
        var_vals = set()
        for datum in data:
            var_vals.add(datum[var_dict[var]])

        for value in var_vals:
            subsets[value] = ({
                'less': [
                    datum for datum in data if datum[var_dict[var]] < value],
                'more': [
                    datum for datum in data if datum[var_dict[var]] >= value],
            })
    else:
        raise Exception('Invalid variable type: %s' % var_type)

    return subsets


def calc_information(data, targ_var, var_dict):
    """
    Calculate the information of a data set.
    If target variable is categorical, the information is entropy.
    If target variable is continuous, the information is variance.
    """
    if not data:
        return 0

    # get entropy or variance, depending on the target variable type
    targ_var_type = targ_var[1]
    if targ_var_type == 'categorical':  # return entropy
        return calc_entropy(data, targ_var, var_dict)

    elif targ_var_type == 'continuous':  # return variance
        dep_arr = [datum[var_dict[targ_var[0]]] for datum in data]
        targ_var_data = np.array(dep_arr)
        return targ_var_data.var()

    else:
        raise Exception('Invalid variable type: %s' % targ_var_type)


def calc_information_of_partition(N, data_subsets, targ_var, var_dict):
    """
    Calculates the information of a partition, which is the weighted
    sum of the information of each subset.

    Information is either entropy or variance, depending on the target
    variable type.
    """
    information = 0
    targ_var_type = targ_var[1]
    for subset in data_subsets.values():
        information += calc_information(
            subset, targ_var, var_dict) * len(subset) / float(N)
    return information


def calc_information_gain(
        information, N, subsets, var_type, targ_var, var_dict):
    """
    For each partition in subsets, the information gain is calculated.

    If var_type is categorical, there is only one partition.
    If var_type is continuous, there are multiple partitions. The value which
    maps to the partition with the best information gain is returned as
    splitval.
    """

    if var_type == 'categorical':
        new_information = calc_information_of_partition(
                N, subsets, targ_var, var_dict)
        info_gain = information - new_information
        splitval = None
    elif var_type == 'continuous':
        max_info_gain = 0
        splitval = None
        for curr_splitval in subsets.keys():
            new_info = calc_information_of_partition(
                    N, subsets[curr_splitval], targ_var, var_dict)
            info_gain = information - new_info
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                splitval = curr_splitval
        info_gain = max_info_gain
    else:
        raise Exception('Invalid variable type: %s' % var_type)

    return info_gain, splitval


def make_tree(
        data, ind_vars, targ_var, var_dict,
        remaining_depth, original_data_size):
    """
    Depth first recursive method used to build a decision tree.

    Note: if remaining_depth is set very large (e.g. 100), then this will
    recur until data is empty, which is one way to terminate a decision tree.
    Check early_termination_pre/post methods for other termination situations.
    """
    # Check for early termination before doing anything else
    early_term = early_termination_pre(
            data, remaining_depth)
    if early_term:
        return None

    # Get information about the current data and store it in node.
    node = Node()
    node.distribution = calc_distribution(data, targ_var, var_dict)
    information = calc_information(data, targ_var, var_dict)

    # Calculate the information gain for each independent variable
    max_info_gain = 0
    next_data = None
    N = len(data)
    for ind_var in ind_vars.keys():
        var = ind_var[0]
        var_type = ind_var[1]
        var_vals = ind_vars[ind_var]

        # Get partitions of data with respect to var
        data_subsets = partition_data(data, var, var_type, var_vals, var_dict)

        # Calculate information gained
        info_gain, splitval = calc_information_gain(
            information, N, data_subsets, var_type, targ_var, var_dict)

        # Update max information and related state variables
        if info_gain > max_info_gain:
            max_info_gain = info_gain

            if var_type == 'continuous':
                variable = (ind_var[0], ind_var[1], splitval)
                data_subsets = data_subsets[splitval]
            elif var_type == 'categorical':
                variable = ind_var
            next_data = data_subsets

    # Check for early termination after looking at potential splits
    early_term = early_termination_post(next_data)
    if early_term:
        return node

    # Using the independent variable with the most info gained, update the
    # current node's decision variable and recursively build its children.
    node.variable = variable
    for value in next_data.keys():
        node.children[value] = make_tree(
            next_data[value],
            ind_vars,
            targ_var,
            var_dict,
            remaining_depth - 1,
            original_data_size)

    # After building children, return tree.
    return node


def write_tree(node, f):
    """
    Recursively writes a tree to 'f'.
    """
    for key in node.children.keys():
        if not node.children[key]:
            node.children.pop(key)

    f.write('%s\n' % str(node))

    for child in node.children.values():
        write_tree(child, f)


def read_tree(filename):
    """
    Recursively builds and returns the decision tree contained in 'filename'.
    """
    pat = re.compile('(None|\([^\)]*\)),(\([^\[\]]*\)|{[^{}]*}),(\[[^\[\]]*\])')
    f = file(filename, 'r')
    root = read_tree_helper(f, pat)
    f.close
    return root


def read_tree_helper(f, pat):
    """
    Recursively builds a decision tree based on the file 'f'.
    If the tree was built properly, there will be no EOFError raised.
    """
    try:
        line = f.next()
    except EOFError as e:
        print 'EOF! Tree is invalid.'
        raise e

    node = Node()
    data = pat.search(line)
    data = data.groups()

    # Set the root's variable and distribution
    node.variable = eval(data[0])
    node.distribution = eval(data[1])

    # Recursively build children
    node.children = {}
    children_keys = eval(data[2])
    for key in children_keys:
        node.children[key] = read_tree_helper(f, pat)
    return node
