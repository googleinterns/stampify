''' Class definition for Pre processed contents'''


class PreprocessedContents:
    def __init__(
            self,
            title_text,
            normal_text,
            media,
            embedded_content,
            quoted_content):
        self.title_text = title_text
        self.normal_text = normal_text
        self.media = media
        self.embedded_content = embedded_content
        self.quoted_content = quoted_content

        self._calculate_content_counts()

    def _calculate_content_counts(self):
        # calculate all counts once so we
        # don't have to recalculate everytime
        # it's needed
        self.title_text_content_count = len(self.title_text)
        self.normal_text_content_count = len(self.normal_text)
        self.media_content_count = len(self.media)
        self.embedded_content_count = len(self.embedded_content)
        self.quoted_content_count = len(self.quoted_content)

    def get_title_text_content_count(self):
        return self.title_text_content_count

    def get_normal_text_content_count(self):
        return self.normal_text_content_count

    def get_media_content_count(self):
        return self.media_content_count

    def get_embedded_content_count(self):
        return self.embedded_content_count

    def get_quoted_content_count(self):
        return self.quoted_content_count
