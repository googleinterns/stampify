"""
   This script starts program for stamp stamp_generation

   Once the summarizer is ready, we can move
   this script to main.py in stampify/

   Command to run:
   /stampify/stamp_generator$ python main_stamp_generation.py
"""

import logging

from stamp_generation import generator_input, stamp_generator

LOGGER = logging.getLogger()
_website = generator_input.get_sample_website()

# Output of summarizer

stamp_pages = generator_input.get_sample_stamp_pages()

generator = stamp_generator.StampGenerator(_website, stamp_pages)
stamp = generator.generate_stamp()

# final_generated_stamp.html has the generated amp-html stamp code

try:
    f = open('final_generated_stamp.html', 'w')
    f.write(stamp)
    f.close()
except (IOError, OSError) as err:
    LOGGER.error(err)
