import itertools
import math
import time

class node(object):
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def has_child(self, item):
        for node in self.children:
            if node.item == item:
                return True
        return False

    def get_child(self, item):
        for node in self.children:
            if node.item == item:
                return node
        return None

    def add_child(self, item):
        child = node(item, 1, self)
        self.children.append(child)
        return child


class tree(object):
    def __init__(self, transactions, minSupCount, root, count):
        self.freq = self.find_freq_itemsets(transactions, minSupCount)
        self.headers = self.build_headers(self.freq)
        self.root = self.build_tree(transactions, root,
            count, self.freq, self.headers)

    @staticmethod
    def find_freq_itemsets(transactions, minSupCount):
        counts = {}
        for trans in transactions:
            for item in trans:
                if item not in counts:
                    counts[item] = 1
                else:
                    counts[item] += 1

        for key in list(counts.keys()):
            if counts[key] < minSupCount:
                del counts[key]

        return counts

    @staticmethod
    def build_headers(freq):

        headers = {}
        for key in freq.keys():
            headers[key] = None

        return headers

    def build_tree(self, transactions, item, count, freq, headers):
        root = node(item, count, None)
        for trans in transactions:
            sorted_items = [x for x in trans if x in freq]
            sorted_items.sort(key = lambda x: freq[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)

        return root

    def insert_tree(self, items, node, headers):
        """Recursively grow tree
        """
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add child.
            child = node.add_child(first)

            # Link it to header
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, headers)
    def has_single_path(self, node):
        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0:
            return True
        else:
            return True and self.has_single_path(node.children[0])

    def mine_patterns(self, minSupCount):
        if self.has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.get_patterns(self.mine_sub_trees(minSupCount))

    def get_patterns(self, patterns):
        suffix = self.root.item

        if suffix is not None:
            # We are in a conditional tree.
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]

            return new_patterns
        return patterns

    def generate_pattern_list(self):
        patterns = {}
        items = self.freq.keys()

        # If we are in a conditional tree,
        # the suffix is a pattern on its own.
        if self.root.item is None:
            suffix_item = []
        else:
            suffix_item = [self.root.item]
            patterns[tuple(suffix_item)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_item))
                patterns[pattern] = \
                    min([self.freq[x] for x in subset])

        return patterns

    def mine_sub_trees(self, minSupCount):
        patterns = {}
        sorted_freq = sorted(self.freq.keys(),
                key=lambda x: self.freq[x])

        # Get items in tree in reverse order of occurrences.
        for item in sorted_freq:
            suffixes = []
            cond_tree_input = []
            node = self.headers[item]

            # Follow node links to get a list of
            # all occurrences of a certain item.
            while node is not None:
                suffixes.append(node)
                node = node.link

            # For each occurrence of the item, 
            # trace the path back to the root node.
            for suffix in suffixes:
                freq = suffix.count
                path = []
                parent = suffix.parent

                while parent.parent is not None:
                    path.append(parent.item)
                    parent = parent.parent

                for i in range(freq):
                    cond_tree_input.append(path)

            # Construct subtree and mine patterns
            subtree = tree(cond_tree_input, minSupCount,
                        item, self.freq[item])
            subtree_patterns = subtree.mine_patterns(minSupCount)

            # Insert subtree patterns into main patterns dictionary.
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]

        return patterns


def find_frequent_patterns(transactions, minSupCount):
    fptree = tree(transactions, minSupCount, None, None)
    return fptree.mine_patterns(minSupCount)

def data_load(filename:str):
    """Load in data from file. Assumed to be comma separated value file
    such as the UCI Census Income Dataset
    (http://archive.ics.uci.edu/ml/datasets/Adult)

    Returns data as 2d list with all values seperated by a comma
    """
    # start = time.time()
    file = open(filename, 'r')
    transactions = file.readlines()
    file.close()
    for i in range(len(transactions)):
        line = transactions[i]
        line = line.strip().rstrip(',')
        line = line.split(',')
        transactions[i] = line

    # end = time.time()
    # print("data loading: ", (end - start))
  
    return transactions

def main(args):
    start = time.time()
    data = data_load(args[0])
    minSupCount = math.ceil(args[1]*len(data))
    patterns = find_frequent_patterns(data, minSupCount)
    print(patterns)
    end = time.time()
    print('total runtime: ', (end - start))

if __name__ == "__main__":
    args = ["Data.csv", .2]
    main(args)