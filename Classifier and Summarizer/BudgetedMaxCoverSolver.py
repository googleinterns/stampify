from itertools import combinations


class Cover:
    '''
    Boiled down representation of a stamp page consists
    of only the cover of elements along with the cost and id.

    All elements are considered to have equal weight.
    '''

    def __init__(self, cover, cost, id, number_of_elements):
        self.cover = cover
        self.cost = cost
        self.number_of_elements = number_of_elements
        # ordinal(index) of the Cover in the whole list - this is very important - remember this
        self.id = id


class BudgetedMaxCover:
    '''
    Consists of related utilities for performing the approximate algorithm for
    budgeted max cover outlined as algorithm 2 in the following paper: 
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.49.5784&rep=rep1&type=pdf
    To find the optimal budget applies binary search and runs the algorithm
    for each instance of the budget
    '''

    def __init__(self, list_of_covers, max_size_allowed, number_of_elements):
        '''
        Initializes the necessary instance variables.

        sets the instance variables to the correct value
        before performing an iteration of the budgeted
        maximum cover algorithm
        '''
        self.list_of_covers = list_of_covers
        self.budget = 0  # budget will be used later on
        self.cover_size = len(list_of_covers)  # number of covers
        self.max_size_allowed = max_size_allowed  # number of covers that can be picked
        # number of elements each cover is over
        self.number_of_elements = number_of_elements

    def pick_cover(self, cover_index):
        '''
        Picks a cover and updates the related variables.

        Given a cover to pick it updates the instance
        variables such as the total cost so far
        and the covers_picked_so_far picked
        '''
        cover_picked = self.list_of_covers[cover_index]  # temporarily store the cover
        self.cost_for_covers_picked_so_far += cover_picked.cost  # update the total cost
        self.covers_picked_so_far.append(
            cover_picked.id)  # update the picked covers

        self.number_of_elements_picked = 0
        for i in range(self.number_of_elements):
            self.is_element_picked[i] |= cover_picked.cover[i]  # bitwise OR
            self.number_of_elements_picked += self.is_element_picked[i]

    def weight_for_uncovered_elements(self, cover_index):
        '''
        For a given cover C finds the number of the elemnts present
        in C but not covered by any other cover in the current list
        of covers.
        Params :
          cover_index : index of the cover in the list_of_covers

        Returns : an integer representing the number of elements covered by 
        the cover_picked but not by an previously chosen cover
        '''
        weight = 0
        cover_picked = self.list_of_covers[cover_index]
        for i in range(self.number_of_elements):
            if cover_picked.cover[i] == 1 and self.is_element_picked[i] == 0:
                weight += 1
        return weight

    def cost_for_picking_element(self, cover_index):
        ''' return the cost of the cover'''
        return self.list_of_covers[cover_index].cost

    def comparator_for_sorting(self, cover_index):
        '''Provides a simple comparator for sorting the unpicked covers'''
        return max(1, self.weight_for_uncovered_elements(cover_index)) / self.cost_for_picking_element(cover_index)

    def initialize_auxiliary_variables(self):
        '''initializes the auxiliary variables'''
        self.cost_for_covers_picked_so_far = 0
        self.number_of_elements_picked = 0
        self.covers_picked_so_far = []
        self.is_element_picked = [0 for i in range(self.number_of_elements)]

    def sum_of_costs_for_covers(self, covers_picked):
        ''' returns the total cost of a given set of covers'''
        total_cost = sum([self.list_of_covers[i].cost for i in covers_picked])
        return total_cost

    def find_max_cover_given_initial_covers(self, initial_covers_picked):
        '''
        Finds the maximum cover given a starting cover.

        Given an initial list of covers to start with,
        iteratively expands the list of covers to cover
        more elements within the given budget
        Params:
          initial_covers_picked = the initial list of covers we start with

        Returns : attriutes for the best set of covers returned as a dict
        '''
        self.initialize_auxiliary_variables()
        for cover in initial_covers_picked:
            self.pick_cover(cover)

        some_cover_can_be_picked = True

        while some_cover_can_be_picked:

            candidate_cover_indices = [i for i in range(self.cover_size)   # find all cover indices such that
                                       # picking it would not exceed budget
                                       if self.list_of_covers[i].cost+self.cost_for_covers_picked_so_far <= self.budget and
                                       self.list_of_covers[i].id not in self.covers_picked_so_far]  # and is not already picked

            candidate_cover_indices.sort(
                key=self.comparator_for_sorting, reverse=True)

            some_cover_can_be_picked = True

            if len(candidate_cover_indices) > 0:
                self.pick_cover(candidate_cover_indices[0])
            else:
                some_cover_can_be_picked = False

        return {
            "weight_of_elements_covered": self.number_of_elements_picked,
            "list_of_covers": self.covers_picked_so_far
        }

    def approximate_maximum_cover_helper(self, budget):
        '''
        A helper function for the approximate maximum cover

        Performs a single run of the Algorithm-2 as outlined
        in the paper mentioned above . The budget is fixed
        for each run.

        Params:
          budget : the maximum cost that can be used for picking covers

        Return type:
          the maximum cover 
        '''
        weight_of_elements_covered_so_far = 0
        max_cover_so_far = []
        self.budget = budget
        k = 3  # k is the minimum size of the subsets to pick. k=3 as per the implementation in the paper

        # generate all subsets of size < k - Phase 1 of the algorithm
        for subset_size in range(1, k):
            subsets_of_size_less_than_k = combinations(
                range(0, len(self.list_of_covers)), subset_size)
            for subset in subsets_of_size_less_than_k:
                if self.sum_of_costs_for_covers(subset) <= self.budget:
                    self.initialize_auxiliary_variables()
                    approx_best_cover_for_size_less_than_k = self.find_max_cover_given_initial_covers(
                        subset)
                    if weight_of_elements_covered_so_far < approx_best_cover_for_size_less_than_k["weight_of_elements_covered"]:
                        weight_of_elements_covered_so_far = approx_best_cover_for_size_less_than_k[
                            "weight_of_elements_covered"]
                        max_cover_so_far = approx_best_cover_for_size_less_than_k["list_of_covers"]

        # generate all subsets for size k=3 and then try to extend - Phase 2 of the algorithm
        subsets_of_size_k = combinations(range(0, len(self.list_of_covers)), k)
        for subset in subsets_of_size_k:
            if self.sum_of_costs_for_covers(subset) <= self.budget:
                approx_best_cover_with_initial_subset = self.find_max_cover_given_initial_covers(
                    subset)
                weight_of_elements_covered = approx_best_cover_with_initial_subset[
                    "weight_of_elements_covered"]
                list_of_covers = approx_best_cover_with_initial_subset["list_of_covers"]

                if weight_of_elements_covered_so_far < weight_of_elements_covered or (weight_of_elements_covered_so_far == weight_of_elements_covered and len(list_of_covers) > len(max_cover_so_far)):
                    weight_of_elements_covered_so_far = weight_of_elements_covered
                    max_cover_so_far = list_of_covers

        return max_cover_so_far

    def find_approximate_maximum_cover(self):
        '''
        for a given list of covers - binary searches
        on the maximum budget such that number of 
        covers picked <= max_size_allowed 
        '''
        lower_bound_for_budget = 1
        upper_bound_for_budget = sum(
            [self.list_of_covers[i].cost for i in range(0, len(self.list_of_covers))])

        best_cover = []
        best_cost = 0

        while lower_bound_for_budget <= upper_bound_for_budget:
            current_budget_fixed = (
                lower_bound_for_budget+upper_bound_for_budget)//2
            approximate_maximum_cover_for_given_budget = self.approximate_maximum_cover_helper(
                current_budget_fixed)
            if len(approximate_maximum_cover_for_given_budget) <= self.max_size_allowed:

                best_cover = approximate_maximum_cover_for_given_budget
                best_cost = current_budget_fixed

                lower_bound_for_budget = current_budget_fixed + 1
            else:
                upper_bound_for_budget = current_budget_fixed - 1

        return {
            "best_cover": [self.list_of_covers[i].id for i in best_cover],
            "best_cost": best_cost
        }
