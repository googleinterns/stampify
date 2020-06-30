''' This Module provides the main interface
for the Summarizer module
'''
from data_models.contents import ContentType
from summarization.extractor_output_preprocessor import SentenceWithAttributes
from summarization.stamp_page_picking.stamp_page_picker import StampPagePicker
from summarization.summarizer_output import StampPage, StampPages
from summarization.text_media_matching.text_media_matcher import \
    TextMediaMatcher


class Summarizer:
    def __init__(
            self,
            title_text_contents,
            normal_text_contents,
            media_contents,
            embedded_contents,
            max_pages_allowed):
        self.title_text_contents = title_text_contents
        self.normal_text_contents = normal_text_contents
        self.media_contents = media_contents
        self.embedded_contents = embedded_contents
        self.max_pages_allowed = max_pages_allowed
        # we don't directly instantiate StampPages
        # object since we need to use the list of
        # stamp pages to cap and pick stamp pages
        self.stamp_pages_list = list()
        self.stamp_pages = StampPages()

        # collect summary sentence embeddings
        self.summary_sentence_embeddings = [
            text.embedding for text in self.normal_text_contents
        ]

    def get_summarized_content(self):
        # first do text media matching
        self._perform_text_media_matching()

        # concat the matched and unmatched contents list
        # and send to make stamp page objects out of them
        self._assemble_and_add_stamp_pages_to_list(
            self.matched_contents + self.unmatched_contents
        )

        # now that the stamp pages have been assembled we
        # can add titles to them
        self._perform_title_media_matching()

        # now we cap the stamp pages themselves
        self._cap_stamp_pages()

        # add the capped stamp pages to the
        # StampPages object that will be returned
        for stamp_page in self.capped_stamp_pages:
            self.stamp_pages.add_stamp_page(stamp_page)

        return self.stamp_pages

    def _cap_stamp_pages(self):
        ''' cap some of the stamp pages and use only
        them in the final stamp story
        '''
        max_cover_solver = StampPagePicker(
            self.stamp_pages_list,
            self.normal_text_contents,
            self.max_pages_allowed
        )
        processed_pages_dict \
            = max_cover_solver.get_capped_and_unused_stamp_pages()
        # these are the stamp pages we'll use
        self.capped_stamp_pages = processed_pages_dict["capped_stamp_pages"]
        # these won't be used in the full stamp pages
        # we keep it for future use or processing
        self.extra_stamp_pages = processed_pages_dict["unused_stamp_pages"]

    def _perform_text_media_matching(self):
        text_media_matcher = TextMediaMatcher(
            self.normal_text_contents,
            self.media_contents
        )
        matched_and_unmatched_content_dict \
            = text_media_matcher._get_matched_and_unmatched_contents()
        # list of tuples (x,y) where x:text and y:media
        self.matched_contents \
            = matched_and_unmatched_content_dict["matched_contents"]
        # list of either sentences or media unmatched
        # we can still use them for stamp pages
        self.unmatched_contents \
            = matched_and_unmatched_content_dict["unused_contents"]

    def _perform_title_media_matching(self):
        ''' find appropriate matchings between
        title text and media
        '''
        title_media_matcher = TextMediaMatcher(
            self.title_text_contents,
            self.media_contents
        )
        matched_and_unmatched_contents_dict \
            = title_media_matcher._get_matched_and_unmatched_contents()

        # for titles we use only the matched contents
        # discard the unmatched contents
        matched_contents \
            = matched_and_unmatched_contents_dict["matched_contents"]

        # from the already formed stamp pages find the
        # ones with media_index in matched_contents
        # and set the overlay_title accordingly
        for sentence_media_pair in matched_contents:
            sentence, media = sentence_media_pair
            for stamp_page_index in range(len(self.stamp_pages_list)):
                if self.stamp_pages_list[stamp_page_index].media_index \
                        == media.content_index:
                    self.stamp_pages_list[stamp_page_index].overlay_title \
                        = sentence.text

    def _assemble_and_add_stamp_pages_to_list(self, content_list):
        '''
        Generates the stamp page and adds it to the
        list of stamp pages
        Params:
            * content_list : contains a list of contents that could be
            matched text and media or just text/media or embedded contents
            gets attributes for different content and instantiates StampPage
        '''
        for content in content_list:
            # get attributes for stamp page object creation
            text, media, embedded, stamp_descriptor_embedding \
                = self._get_attribute_for_contents(content)
            stamp_page = self._assemble_and_instantiate_stamp_page(
                text=text,
                media=media,
                embedded=embedded,
                stamp_descriptor_embedding=stamp_descriptor_embedding
            )
            self.stamp_pages_list.append(stamp_page)

    def _get_attribute_for_contents(self, content):
        ''' returns attributes from content for
        stamp page object creation
        '''
        # initialize all attributes to None
        # some of them may not be used
        text = None
        media = None
        embedded = None
        stamp_descriptor_embedding = None

        if isinstance(content, tuple):
            # if its a tuple its matched
            # text and media together
            text, media = content
            stamp_descriptor_embedding = text.embedding

        elif isinstance(content, SentenceWithAttributes):
            # text will be an object of type
            # SentenceWithAttributes
            text = content
            stamp_descriptor_embedding = text.embedding
        else:
            # it's either just media or is an
            # embedded content
            if content.content_type == ContentType.IMAGE:
                media = content
                stamp_descriptor_embedding = media.img_description_embedding
            else:
                embedded = content

        return text, media, embedded, stamp_descriptor_embedding

    def _assemble_and_instantiate_stamp_page(
            self,
            text=None,
            media=None,
            embedded=None,
            stamp_descriptor_embedding=None):
        ''' instantiates and returns a stamp page instance'''
        # define everything necessary for a stamp page object
        media_index = -1
        sentence_index = -1
        is_embedded_content = False
        overlay_title = None
        overlay_text = None
        overlay_font_style = None
        overlay_font_size = None
        stamp_position = -1

        if text:
            sentence_index = text.index
            overlay_text = text.text
            overlay_font_style = text.font_style

        if embedded:
            is_embedded_content = True
            media_index = embedded.content_index

        if media:
            media_index = media.content_index

        return StampPage(
            media_index,
            sentence_index,
            is_embedded_content,
            overlay_title,
            overlay_text,
            overlay_font_style,
            overlay_font_size,
            stamp_position,
            stamp_descriptor_embedding
        )
