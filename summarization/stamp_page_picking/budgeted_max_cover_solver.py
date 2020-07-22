'''Budgeted Maximum Cover Solver

This module contains an approximate algoritm for solving
the budgeted maximum cover algorithm.

This script contains the following classes:
    * Cover : to represent the cover over elements(sentences)
    * BudgetedMaxCover : the class containing the solver

The solver accepts a list of elements of type Cover
'''

from itertools import combinations

from data_models.summarizer_output import StampPageType


class BudgetedMaxCoverSolver:
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
        self.max_size_allowed = max_size_allowed  # covers allowed
        # number of elements each cover is over
        self.number_of_elements = number_of_elements
        self.cost_for_covers_picked_so_far = 0
        self.number_of_elements_picked = 0
        self.covers_picked_so_far = []
        self.is_element_picked = []

    def find_approximate_maximum_cover(self):
        '''
        for a given list of covers - binary searches
        on the maximum budget such that number of
        covers picked <= max_size_allowed
        '''
        lower_bound_for_budget = 0.0
        upper_bound_for_budget = self._sum_of_costs_for_covers(
            list(range(len(self.list_of_covers))))

        # smallest change is 1/(score for the stamp page with maximum score)
        delta = 1 / StampPageType.get_stamp_type_score(
                StampPageType.MEDIA_WITH_TEXT_AND_TITLE)

        best_cover = []
        best_cost = 0

        while lower_bound_for_budget <= upper_bound_for_budget:
            current_budget_fixed = (
                lower_bound_for_budget+upper_bound_for_budget)/2

            approximate_maximum_cover_for_given_budget \
                = self._approximate_maximum_cover_helper(current_budget_fixed)

            if self._size_is_ok(approximate_maximum_cover_for_given_budget):

                best_cover = approximate_maximum_cover_for_given_budget
                best_cost = current_budget_fixed

                lower_bound_for_budget = current_budget_fixed + delta
            else:
                upper_bound_for_budget = current_budget_fixed - delta

        return {
            "best_cover": [self.list_of_covers[i].id for i in best_cover],
            "best_cost": best_cost
        }

    def _pick_cover(self, cover_index):
        '''
        Picks a cover and updates the related variables.

        Given a cover to pick it updates the instance
        variables such as the total cost so far
        and the covers_picked_so_far picked
        '''
        cover_picked = self.list_of_covers[cover_index]
        self.cost_for_covers_picked_so_far += cover_picked.cost
        self.covers_picked_so_far.append(
            cover_picked.id)  # update the picked covers

        self.number_of_elements_picked = 0
        for i in range(self.number_of_elements):
            self.is_element_picked[i] |= cover_picked.cover[i]  # bitwise OR
            self.number_of_elements_picked += self.is_element_picked[i]

    def _weight_for_uncovered_elements(self, cover_index):
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

    def _cost_for_picking_element(self, cover_index):
        ''' return the cost of the cover'''
        return self.list_of_covers[cover_index].cost

    def _unpicked_weights_to_cost_ratio(self, cover_index):
        '''Provides a simple weight:cost ratio for a covers'''
        return max(1, self._weight_for_uncovered_elements(cover_index)) \
            / self._cost_for_picking_element(cover_index)

    def _initialize_auxiliary_variables(self):
        '''initializes the auxiliary variables'''
        self.cost_for_covers_picked_so_far = 0
        self.number_of_elements_picked = 0
        self.covers_picked_so_far = []
        self.is_element_picked = [0]*self.number_of_elements

    def _sum_of_costs_for_covers(self, covers_picked):
        ''' returns the total cost of a given set of covers'''
        return sum(self.list_of_covers[i].cost for i in covers_picked)

    def _cover_can_be_picked(self, cover_index):
        ''' returns True if cover can be picked for given budget'''
        cost_if_picked \
            = self.list_of_covers[cover_index].cost \
            + self.cost_for_covers_picked_so_far

        is_not_picked \
            = self.list_of_covers[cover_index].id not in \
            self.covers_picked_so_far

        return cost_if_picked <= self.budget and is_not_picked

    def _find_max_cover_given_initial_covers(self, initial_covers_picked):
        '''
        Finds the maximum cover given a starting cover.

        Given an initial list of covers to start with,
        iteratively expands the list of covers to cover
        more elements within the given budget
        Params:
          initial_covers_picked = the initial list of covers we start with

        Returns : attriutes for the best set of covers returned as a dict
        '''
        self._initialize_auxiliary_variables()
        for cover in initial_covers_picked:
            self._pick_cover(cover)

        some_cover_can_be_picked = True

        while some_cover_can_be_picked:

            candidate_cover_indices \
                = [i for i in range(self.cover_size)
                   if self._cover_can_be_picked(cover_index=i)]

            some_cover_can_be_picked = True

            if candidate_cover_indices:
                self._pick_cover(
                    max(candidate_cover_indices,
                        key=self._unpicked_weights_to_cost_ratio)
                )
            else:
                some_cover_can_be_picked = False

        return {
            "weight_of_cover": self.number_of_elements_picked,
            "list_of_covers": self.covers_picked_so_far
        }

    def _perform_max_cover_on_subset(self, subset):
        approx_best_cover_for_subset \
            = self._find_max_cover_given_initial_covers(subset)

        weight_of_cover \
            = approx_best_cover_for_subset["weight_of_cover"]

        list_of_covers \
            = approx_best_cover_for_subset["list_of_covers"]

        if self.weight_of_elements_covered_so_far < weight_of_cover or \
            (self.weight_of_elements_covered_so_far == weight_of_cover
             and len(list_of_covers) > len(self.max_cover_so_far)):
            self.weight_of_elements_covered_so_far = weight_of_cover
            self.max_cover_so_far = list_of_covers

    def _approximate_maximum_cover_helper(self, budget):
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
        self.weight_of_elements_covered_so_far = 0
        self.max_cover_so_far = []
        self.budget = budget
        k = 3  # k is the minimum size of the subsets to pick

        # generate all subsets of size < k - Phase 1 of the algorithm
        for subset_size in range(1, k):
            subsets_of_size_less_than_k = combinations(
                range(0, len(self.list_of_covers)), subset_size)

            for subset in subsets_of_size_less_than_k:
                if self._sum_of_costs_for_covers(subset) > self.budget:
                    continue
                aggregated_cover = [0]*self.number_of_elements
                for cover_index in subset:
                    aggregated_cover \
                        = [a | b for a, b in zip(
                            aggregated_cover,
                            self.list_of_covers[cover_index].cover)]

                if sum(aggregated_cover) \
                    > self.weight_of_elements_covered_so_far \
                    or (sum(aggregated_cover)
                        == self.weight_of_elements_covered_so_far
                        and len(subset) > len(self.max_cover_so_far)):

                    self.weight_of_elements_covered_so_far \
                        = sum(aggregated_cover)
                    self.max_cover_so_far = subset

        # generate all subsets for size k=3 and then try to extend
        subsets_of_size_k = combinations(range(0, len(self.list_of_covers)), k)

        for subset in subsets_of_size_k:
            if self._sum_of_costs_for_covers(subset) > self.budget:
                continue
            self._perform_max_cover_on_subset(subset)

        return self.max_cover_so_far

    def _size_is_ok(self, list_of_covers):
        ''' returns true if the size is ok for a cover'''
        return len(list_of_covers) <= self.max_size_allowed
