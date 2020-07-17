''' Class definition for SentenceWithAttributes object'''


class SentenceWithAttributes:
    ''' Object to represent a summary sentence
    or title sentence along with attributes such as
    embedding or font_style
    '''

    def __init__(
            self,
            text,
            paragraph_index,
            sentence_index_in_para,
            sentence_weight,
            font_style,
            embedding):
        self.text = text
        self.paragraph_index = paragraph_index
        self.sentence_index_in_para = sentence_index_in_para
        self.sentence_weight = sentence_weight
        self.font_style = font_style
        self.embedding = embedding

    def get_weighted_index(self):
        return self.paragraph_index \
            + self.sentence_index_in_para * self.sentence_weight
