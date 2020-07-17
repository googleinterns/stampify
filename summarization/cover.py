''' Module to define the Cover object used
in budgeted max cover solver
'''


class Cover:
    '''
    Boiled down representation of a stamp page consists
    of only the cover of elements along with the cost and id.

    All elements are considered to have equal weight.
    Attributes:
        * cover : a list of size number_of_elements
            consist of 1's and 0's . 1 is present in the
            ith index if the ith summary sentence is well
            described by the stamp page's descriptor
            0 otherwise.

        * cost : a cost assigned for the stamp page
            depends on the type of stamp page. Higher
            the visual content lower is the cost of the
            stamp page. cost could also be considered
            as penalty

        * number_of_elements : is the number of summary
            sentences the cover is over

        * id : index or ordinal of the stamp page.
            will be used for ordering
    '''

    def __init__(self, cover, cost, id, number_of_elements):
        self.cover = cover
        self.cost = cost
        self.number_of_elements = number_of_elements
        self.id = id  # ordinal (index)
