''' Module for scoring utils '''


class ScoringUtils:
    SCORE_FOR_TEXT_ONLY_STAMP = 1.0
    SCORE_FOR_EMBEDDED_STAMP = 5.0
    SCORE_FOR_VISUAL_STAMP = 10.0

    def __init__(self, stamp_pages, stamp_page_covers, cover_size):
        self.stamp_pages = stamp_pages
        self.stamp_page_covers = stamp_page_covers
        self.cover_size = cover_size
        self.picked_cover = [0] * self.cover_size

        self.last_picked_stamp_page_index = -1

        self.individual_score_weights = {
            "content_change": 1,
            "unpicked_weights_to_cost": 1,
            "content_type": 1
        }

    def update_last_picked_stamp_page(self, stamp_index):
        self.last_picked_stamp_page_index = stamp_index

    def interestingess_metric(self, stamp_page_index):
        '''
        calculates the interesting-ness metric based
        on the last picked stamp page
        '''
        from_stamp_page_index = self.last_picked_stamp_page_index
        to_stamp_page_index = stamp_page_index

        content_change_score \
            = self._get_content_change_score(
                from_stamp_page_index,
                to_stamp_page_index
            )

        unpicked_weight_cost_ratio_score \
            = self._get_unpicked_weights_to_cost_ratio_score(stamp_page_index)

        content_type_score = self._get_content_type_score(stamp_page_index)

        return self._compute_weighted_score(
            {
                "content_change": content_change_score,
                "unpicked_weights_to_cost": unpicked_weight_cost_ratio_score,
                "content_type": content_type_score
            }
        )

    def _get_content_type_score(self, stamp_page_index):
        stamp_page = self.stamp_pages[stamp_page_index]
        if stamp_page.is_embedded_content:
            return self.SCORE_FOR_EMBEDDED_STAMP
        elif stamp_page.media_index != -1:
            return self.SCORE_FOR_VISUAL_STAMP
        else:
            return self.SCORE_FOR_TEXT_ONLY_STAMP

    def pick_stamp_page_cover_at_index(self, index):
        # update the picked_cover
        for i in range(self.cover_size):
            self.picked_cover[i] \
                = self.picked_cover[i] | self.stamp_page_covers[index].cover[i]

    def _get_content_change_score(self, from_index, to_index):
        # higher change in content type is better
        return (1 if
                self._get_stamp_page_type(from_index)
                != self._get_stamp_page_type(to_index) else 0
                )

    def _get_unpicked_weights_to_cost_ratio_score(self, index):
        total_weight = 0
        for i in range(self.cover_size):
            if self.picked_cover[i] == 0 \
                    and self.stamp_page_covers[index].cover[i] == 1:
                total_weight += 1
        return total_weight / self.stamp_page_covers[index].cost

    def _compute_weighted_score(self, score_list):
        weighted_score = 0
        for score_type, weight in self.individual_score_weights.items():
            weighted_score += score_list[score_type] * weight

        return weighted_score

    def _get_stamp_page_type(self, stamp_page_index):
        # assign a number to each stamp page type
        stamp_page = self.stamp_pages[stamp_page_index]
        if stamp_page.is_embedded_content:
            return 4
        elif stamp_page.media_index != -1 and stamp_page.sentence_index != -1:
            return 3
        elif stamp_page.media_index != -1:
            return 2
        elif stamp_page.sentence_index != -1:
            return 1
