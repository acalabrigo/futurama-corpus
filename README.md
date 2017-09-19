# The Futurama Corpus

This repo contains a corpus of dialogue spoken on the television show Futurama. The corpus itself is found in data/futurama_scripts.txt, and the futurama_parse.py module is included to allow easy access to the dialogue, by character. This corpus was created by scraping the Futurama scripts available [here](https://theinfosphere.org), which include 7 seasons of the show and 4 movies. Unfortunately, the website moderators got a little lazy with the formatting of the last season, so many of those scripts could not be parsed. The futurama_scrape.py script was used to scrape the scripts.

Below is a breakdown of the corpus by major character:
- Fry: 34,805 words
- Bender: 30,333 words
- Leela: 28,993 words
- Farnsworth: 16,936 words
- Hermes: 8,095 words
- Zoidberg: 7,201 words
- Amy: 6,582 words

The included futurama_generator.py script shows just one example of an application of this corpus. This script randomly generates dialogue from the character Fry using a simple 5-gram model with some rule filtering. My hope is that others may find some fun with this corpus for future NLP projects.
