''' This script defines the object structure
for the output(s) of the summarizer and provides
methods to access the data as required'''


class StampPages:
    '''Object structure to store the Stamp Pages'''

    def __init__(self):
        self.stamp_pages = list()

    def add_stamp_page(self, stamp_page):
        ''' adds stamp pages to the list'''
        self.stamp_pages.append(stamp_page)

    def get_formatted_list(self):
        ''' returns the list of objects formatted as a
        list of dicts
        '''
        formatted_list = list()
        for stamp_page in self.stamp_pages:
            formatted_list.append(stamp_page.get_formatted_dict())
        return formatted_list


class StampPage:
    '''Object structure for a Stamp Page

    This object structure will be used to define
    a Stamp Page required as the output of the Summarizer.
    This Stamp Page object will be passed on to the
    generator which will assemble the final stamp page.

    Attributes:
    * media_index : index of the media(image/video/insta) as
    defined in the Contents List passed to classifier

    * sentence_index : index of the sentence as defined
    in the Contents List passed to classifier

    * is_embedded_content : True if the media is embedded
    ( instagram post / tweets / pinterest etc)

    * overlay_title : overlay title for stamp page

    * overlay_text : overlay text for stamp page

    * overlay_font_style and overlay_font_size : taken
    as it appears on the webpage

    * stamp_position: The order or index of the stamp in the final
    collected of stamp pages

    * stanp_descriptor_embedding : the embedding of the text
    that will be used to describe the stamp page. This depends
    on the type of stamp page it is.
    '''

    def __init__(
            self,
            media_index,
            sentence_index,
            is_embedded_content,
            overlay_title,
            overlay_text,
            overlay_font_style,
            overlay_font_size,
            stamp_position,
            stamp_descriptor_embedding):
        self.media_index = media_index
        self.sentence_index = sentence_index
        self.is_embedded_content = is_embedded_content
        self.overlay_title = overlay_title
        self.overlay_text = overlay_text
        self.overlay_font_style = overlay_font_style
        self.overlay_font_size = overlay_font_size
        self.stamp_position = stamp_position
        self.stamp_descriptor_embedding = stamp_descriptor_embedding

    def get_formatted_dict(self):
        ''' Returns the object as a formatted dict'''
        if hasattr(self, '__dict__'):
            return self.__dict__
        return {}
