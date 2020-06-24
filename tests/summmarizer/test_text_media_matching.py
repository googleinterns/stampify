from classifier_and_summarizer.summarization.text_media_matching import \
    stable_matcher


def test_stable_matching():
    ''' Tests if the stable matching algorithm produces
    the right output
    '''
    preference_matrix_1 = [[0, 2, 1, 3], [
        2, 3, 0, 1], [3, 1, 2, 0], [2, 1, 0, 3]]
    preference_matrix_2 = [[1, 0, 2, 3], [
        3, 0, 1, 2], [0, 2, 1, 3], [1, 2, 0, 3]]
    stable_matcher_util \
        = stable_matcher.StableMatcher(
            preference_matrix_1,
            preference_matrix_2,
            4)
    expected_matching = [(0, 0), (3, 1), (2, 2), (1, 3)]
    actual_matching = stable_matcher_util.get_matching()
    assert expected_matching == actual_matching
