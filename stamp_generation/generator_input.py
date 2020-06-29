"""
This script contains factory methods to get the input for generator
This script can be removed later when the summarizer is ready.
"""

from data_models.contents import Contents
from data_models.embedded_instagram_post import EInstagramPost
from data_models.embedded_pinterest_pin import EPinterestPin
from data_models.embedded_tweet import ETweet
from data_models.embedded_youtube_video import EYouTubeVideo
from data_models.image import Image
from data_models.quote import Quote
from data_models.text import Text
from data_models.video import Video
from data_models.website import Website
from summarization.summarizer_output import StampPage, StampPages


def get_sample_website():
    _website = Website('https://im.whatshot.in/')

    contents_list = Contents()
    content1 = Text('This is title of website', 'title')
    content2 = Image(img_url='https://im.whatshot.in/'
                             'img/2020/Mar/h-1584953735.jpg',
                     img_height=100, img_width=100, is_gif=False,
                     img_caption=None, img_title="Image Title")

    content3 = Image(img_url='https://hbr.org/resources/images/'
                             'article_assets/2015/02/'
                             'FEB15_05_hbr_nguyen_img_074.jpg',
                     img_height=260, img_width=300, is_gif=False,
                     img_caption="Image Caption", img_title=None)

    content4 = Image(img_url='https://s3.scoopwhoop.com/'
                             'anj/fnnygifs/294761309.gif',
                     img_height=0, img_width=0, is_gif=True,
                     img_caption=None, img_title=None)

    content5 = Video(urls=['https://dafftube.org/wp-content/uploads/'
                           '2014/01/Sample_1280x720_mp4.mp4'],
                     height=0, width=0)

    content6 = ETweet(tweet_id='638793490521001985')
    content7 = EYouTubeVideo(video_id='Fs1fabWUmDM')
    content8 = EInstagramPost(code="1totVhIFXl")
    content9 = EPinterestPin(url="https://www.pinterest.com/"
                                 "pin/573505333797181671/")
    content10 = Quote(q_content="No one gets punished "
                                "for corruption in our country.",
                      cite="Arvind Kejriwal")

    contents_list.add_content(content1)
    contents_list.add_content(content2)
    contents_list.add_content(content3)
    contents_list.add_content(content4)
    contents_list.add_content(content5)
    contents_list.add_content(content6)
    contents_list.add_content(content7)
    contents_list.add_content(content8)
    contents_list.add_content(content9)
    contents_list.add_content(content10)

    _website.set_contents(contents_list)

    return _website


def get_sample_stamp_pages():
    stamp_pages_list = StampPages()
    """
    The first index will be having a title content for the stamp_page,
    which can be included later.
    """

    page1 = StampPage(media_index=1,
                      sentence_index=0,
                      is_embedded_content=False,
                      overlay_title='India has approved the combination '
                      'of two antiviral drugs used to treat HIV,'
                      ' lopinavir and ritonavir',
                      overlay_text='This section is for overlay text',
                      overlay_font_style='',
                      overlay_font_size=16, stamp_position=0,
                      stamp_descriptor_embedding=None)

    page2 = StampPage(media_index=2,
                      sentence_index=0,
                      is_embedded_content=False,
                      overlay_title='This is page2 title',
                      overlay_text='India has approved the combination of two '
                      'antiviral drugs used to treat HIV, lopinavir and '
                      'ritonavir (400 mg and 100 mg, respectively), to '
                      'treat Covid-19, but the first major study of Covid-19 '
                      'treatment published in the New England Journal of '
                      'Medicine (NEJM) found it did not work on severely '
                      'ill patients in China.\n India has approved the '
                      'combination of two antiviral drugs used to treat HIV, '
                      'lopinavir and ritonavir (400 mg and 100 mg, '
                      'respectively), to treat Covid-19, but the first major '
                      'study of Covid-19 treatment published in the New '
                      'England Journal of Medicine (NEJM) found '
                      'it did not work on severely ill patients in China.',
                      overlay_font_style='',
                      overlay_font_size=16, stamp_position=1,
                      stamp_descriptor_embedding=None)

    page3 = StampPage(media_index=3,
                      sentence_index=0,
                      is_embedded_content=False,
                      overlay_title='This is page3 title',
                      overlay_text='Checking how it works for gifs',
                      overlay_font_style='',
                      overlay_font_size=16, stamp_position=2,
                      stamp_descriptor_embedding=None)

    page4 = StampPage(media_index=4,
                      sentence_index=0,
                      is_embedded_content=False,
                      overlay_title='This is page4 title',
                      overlay_text='It contains a video',
                      overlay_font_style='',
                      overlay_font_size=16, stamp_position=3,
                      stamp_descriptor_embedding=None)

    page5 = StampPage(media_index=5,
                      sentence_index=0,
                      is_embedded_content=True,
                      overlay_title='',
                      overlay_text='',
                      overlay_font_style='',
                      overlay_font_size=0, stamp_position=4,
                      stamp_descriptor_embedding=None)

    page6 = StampPage(media_index=6,
                      sentence_index=0,
                      is_embedded_content=True,
                      overlay_title='',
                      overlay_text='',
                      overlay_font_style='',
                      overlay_font_size=0, stamp_position=5,
                      stamp_descriptor_embedding=None)

    page7 = StampPage(media_index=7,
                      sentence_index=0,
                      is_embedded_content=True,
                      overlay_title='',
                      overlay_text='',
                      overlay_font_style='',
                      overlay_font_size=0, stamp_position=6,
                      stamp_descriptor_embedding=None)

    page8 = StampPage(media_index=8,
                      sentence_index=0,
                      is_embedded_content=True,
                      overlay_title='',
                      overlay_text='',
                      overlay_font_style='',
                      overlay_font_size=0, stamp_position=7,
                      stamp_descriptor_embedding=None)

    page9 = StampPage(media_index=9,
                      sentence_index=0,
                      is_embedded_content=False,
                      overlay_title='Today\'s Quotations',
                      overlay_text='This page contains '
                                   'quotation as main content.',
                      overlay_font_style='',
                      overlay_font_size=0, stamp_position=8,
                      stamp_descriptor_embedding=None)

    stamp_pages_list.add_stamp_page(page1)
    stamp_pages_list.add_stamp_page(page2)
    stamp_pages_list.add_stamp_page(page3)
    stamp_pages_list.add_stamp_page(page4)
    stamp_pages_list.add_stamp_page(page5)
    stamp_pages_list.add_stamp_page(page6)
    stamp_pages_list.add_stamp_page(page7)
    stamp_pages_list.add_stamp_page(page8)
    stamp_pages_list.add_stamp_page(page9)

    return stamp_pages_list
