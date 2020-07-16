''' This Module provides the main interface
for the Summarizer module
'''
import json

from data_models.contents import ContentType
from summarization.extractor_output_preprocessor import SentenceWithAttributes
from summarization.stamp_page_picking.stamp_page_picker import StampPagePicker
from summarization.summarizer_output import StampPage, StampPages
from summarization.text_media_matching.text_media_matcher import \
    TextMediaMatcher


class Summarizer:
    ''' Summarizer module for performing
    the various functions for summarizing
    the contents of the webpage
    '''
    SIGNED_DIFFERENCE = "signed-difference"
    CAPPING_METHOD = "interesting-sequence-picker"

    def __init__(
            self,
            contents,
            max_pages_allowed,
            title_topic_is_plural=False):
        self.contents = contents
        self.max_pages_allowed = max_pages_allowed
        # we don't directly instantiate StampPages
        # object since we need to use the list of
        # stamp pages to cap and pick stamp pages
        self.stamp_pages_list = list()
        self.stamp_pages = StampPages()

        # collect summary sentence embeddings
        self.summary_sentence_embeddings = [
            text.embedding for text in self.contents.normal_text
        ]

        # used to determine whether the webpages
        # is about one broad topic or multiple small topics
        self.title_topic_is_plural = title_topic_is_plural

    def _strip_title_and_make_stamp(self):
        ''' This method strips the first item
        which is the webpage title and makes a
        stamp page accordingly so it will be used
        as the seed stamp for the interesting
        sequence
        '''
        if self.CAPPING_METHOD == "interesting-sequence-picker":
            # we only need the seed title if we use
            # interesting sequence picker
            # we put it as the first member of the list
            self._assemble_and_add_stamp_pages_to_list(
                [self.contents.title_text[0]]
            )
        # pop the title accordingly so it won't
        # be used for title media matching
        self.contents.title_text.pop(0)

    def get_summarized_content(self):
        ''' Summarizes the contents of the
        webpage and returns it as a StampPage object
        '''

        # strip title text
        self._strip_title_and_make_stamp()
        # filter images with text as they shouldn't be
        # used for text-media matching
        self._create_stamps_and_filter_images_with_text()

        if self.title_topic_is_plural:
            self._perform_title_first_matching()
        else:
            self._perform_text_first_matching()

        # fetch embeddings for embedded content types
        self._fetch_and_set_stamp_descriptors_dict_for_embedded_content()

        # now add the embedded content for stamp pages
        # if embedded contents are empty no stamp pages
        # will be initialized
        self._assemble_and_add_stamp_pages_to_list(
            self.contents.embedded_content
        )

        # now add the quoted content for stamp pages
        # if quoted contents are empty no stamp
        # pages will be initialized
        self._assemble_and_add_stamp_pages_to_list(
            self.contents.quoted_content
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
        stamp_page_picker = StampPagePicker(
            self.stamp_pages_list,
            self.contents.normal_text,
            self.max_pages_allowed,
            capping_method="interesting-sequence-picker"
        )
        processed_pages_dict \
            = stamp_page_picker.get_capped_and_unused_stamp_pages()
        # these are the stamp pages we'll use
        self.capped_stamp_pages = processed_pages_dict["capped_stamp_pages"]
        # these won't be used in the full stamp pages
        # we keep it for future use or processing
        self.extra_stamp_pages = processed_pages_dict["unused_stamp_pages"]

    def _perform_text_first_matching(self):
        ''' Method to perform text-first matching

        * First finds the normal-text and media matching
            and instantiated the stamp pages with this content
        * Then finds title media matching and tries to pair it
            with the already instantiated stamp pages

        This is done when the topic plurality of the
        webpage is a single broad topic and not many

        '''
        contents_dict_from_text_media_matching \
            = self._perform_text_media_matching()

        contents_dict_from_title_media_matching \
            = self._perform_title_media_matching()

        matched_text_media \
            = contents_dict_from_text_media_matching["matched_contents"]
        unmatched_content \
            = contents_dict_from_text_media_matching["unused_contents"]

        self._assemble_and_add_stamp_pages_to_list(
            matched_text_media + unmatched_content
        )

        matched_title_media \
            = contents_dict_from_title_media_matching["matched_contents"]

        for sentence_media_pair in matched_title_media:
            sentence, media = sentence_media_pair
            for stamp_page_index in range(len(self.stamp_pages_list)):
                if self.stamp_pages_list[stamp_page_index].media_index \
                        == media.content_index:
                    self.stamp_pages_list[stamp_page_index].overlay_title \
                        = sentence.text

    def _perform_title_first_matching(self):
        ''' Method to perform title first matching

        * First find the matchings between media
            and title text. take only the MATCHED
            contents and initialize stamp pages
            accordingly.
        * Then match text and media - take the unmatched
            contents and if there is a correspoding stamp
            page with same media - apply overlay title
            else just add it to the stamp page later
        '''
        contents_dict_from_title_media_matching \
            = self._perform_title_media_matching()

        contents_dict_from_text_media_matching \
            = self._perform_text_media_matching()

        matched_title_media \
            = contents_dict_from_title_media_matching["matched_contents"]

        self._assemble_and_add_stamp_pages_to_list(
            matched_title_media,
            text_is_title_content=True)

        matched_text_media \
            = contents_dict_from_text_media_matching["matched_contents"]
        unmatched_content \
            = contents_dict_from_text_media_matching["unused_contents"]

        # we should filter out plain media which has already been used in some
        # stamp page and should not directly add it to unmatched contents
        if contents_dict_from_text_media_matching["unused_content_type"] \
                == "media":
            already_used_media_indices = [
                title_media_pair[1].content_index
                for title_media_pair in matched_title_media
            ]

            unmatched_content = [
                content for content in unmatched_content
                if content.content_index not in already_used_media_indices
            ]

        for sentence_media_pair in matched_text_media:
            sentence, media = sentence_media_pair
            sentence_media_pair_has_existing_stamp = False
            for stamp_page_index in range(len(self.stamp_pages_list)):
                if self.stamp_pages_list[stamp_page_index].media_index \
                        == media.content_index:
                    self.stamp_pages_list[stamp_page_index].overlay_text \
                        = sentence.text

                    sentence_media_pair_has_existing_stamp = True

            if not sentence_media_pair_has_existing_stamp:
                unmatched_content.append(sentence_media_pair)

        self._assemble_and_add_stamp_pages_to_list(unmatched_content)

    def _perform_text_media_matching(self):
        text_media_matcher = TextMediaMatcher(
            self.contents.normal_text,
            self.contents.media,
        )
        return text_media_matcher._get_matched_and_unmatched_contents()

    def _perform_title_media_matching(self):
        ''' find appropriate matchings between
        title text and media
        '''
        title_media_matcher = TextMediaMatcher(
            self.contents.title_text,
            self.contents.media,
            self.SIGNED_DIFFERENCE
        )
        return title_media_matcher._get_matched_and_unmatched_contents()

    def _assemble_and_add_stamp_pages_to_list(
            self, content_list, text_is_title_content=False):
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
            text, media, embedded, quote, stamp_descriptor_embedding \
                = self._get_attribute_for_contents(content)
            stamp_page = self._assemble_and_instantiate_stamp_page(
                text=text,
                media=media,
                embedded=embedded,
                quote=quote,
                stamp_descriptor_embedding=stamp_descriptor_embedding,
                text_is_title_content=text_is_title_content
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
        quote = None
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

            elif content.content_type == ContentType.QUOTE:
                quote = content
                stamp_descriptor_embedding = quote.embedding
            else:
                embedded = content
                stamp_descriptor_embedding \
                    = self._get_stamp_descriptor_for_embedded_content(content)

        return text, media, embedded, quote, stamp_descriptor_embedding

    def _assemble_and_instantiate_stamp_page(
            self,
            text=None,
            media=None,
            embedded=None,
            quote=None,
            stamp_descriptor_embedding=None,
            text_is_title_content=False):
        ''' instantiates and returns a stamp page instance'''
        # define everything necessary for a stamp page object
        media_index = -1
        para_index = -1
        sentence_in_para_index = -1
        sentence_in_para_weight = 0
        is_embedded_content = False
        is_quoted_content = False
        overlay_title = None
        overlay_text = None
        overlay_font_style = None
        overlay_font_size = None
        stamp_position = -1

        if text:
            para_index = text.paragraph_index
            sentence_in_para_index = text.sentence_index_in_para
            sentence_in_para_weight = text.sentence_weight

            if text_is_title_content:
                overlay_title = text.text
            else:
                overlay_text = text.text
                overlay_font_style = text.font_style

        if quote:
            is_quoted_content = True
            # generator renders quotes considering
            # it as media
            media_index = quote.content_index

        if embedded:
            is_embedded_content = True
            media_index = embedded.content_index

        if media:
            if media.has_text_on_image:
                # this is done mainly to ensure
                # the cost for this type of stamp
                # is chosen appropriately
                overlay_text = ""
            media_index = media.content_index

        return StampPage(
            media_index,
            para_index,
            sentence_in_para_index,
            sentence_in_para_weight,
            is_embedded_content,
            is_quoted_content,
            overlay_title,
            overlay_text,
            overlay_font_style,
            overlay_font_size,
            stamp_position,
            stamp_descriptor_embedding
        )

    def _fetch_and_set_stamp_descriptors_dict_for_embedded_content(self):
        # don't load if there are no embedded contents
        if len(self.contents.embedded_content) == 0 \
                and len(self.contents.quoted_content) == 0:
            return

        self.embedded_descriptors_dict = dict()
        file_path = 'summarization/stamp_descriptors_for_embedded_content.json'
        with open(file_path, 'r') as file:
            # the keys in this dict are of type str() and are
            # no longer of type int
            self.embedded_descriptors_dict = json.load(file)

    def _get_stamp_descriptor_for_embedded_content(self, content):
        # type casting is required since the dict keys
        # are now of type str
        return self.embedded_descriptors_dict[str(content.content_type)]

    def _create_stamps_and_filter_images_with_text(self):
        ''' Filters the images with text as they
        should not be used in text-media matching
        '''
        self._assemble_and_add_stamp_pages_to_list([
            media for media in self.contents.media
            if media.has_text_on_image
        ])

        self.contents.media = [
            media for media in self.contents.media
            if not media.has_text_on_image
        ]
