"""Test of text translation"""

import sys
from enum import Enum
from typing import List, Tuple

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Sections of input text are 'marked' with a maker label, e.g.,
# author: Pablo Neruda
# EOF is a pseudo-marker that we get at the end of the input
#
class Tag(Enum):
    title = "title"
    author = "author"
    translator = "translator"
    book = "book"
    original = "o"
    translation = "t"
    blank = "::Returned for a blank line"
    EOF = "::Returned at end of file"
    ERROR = "::If we couldn't make sense of a line"

tags = [tag.value for tag in Tag]

class Lexer:
    """Lexical state must be encapsulated in an object rather
    than global to the module to allow
    concurrent instances of the parser.
    """
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.pos = 0
        log.debug(f"Initialized {len(self.lines)} lines")

    def next(self) -> Tuple[Tag, str]:
        log.debug("Getting token")
        if self.pos >= len(self.lines):
            log.debug("Reached end")
            return (Tag.EOF, "")
        line = self.lines[self.pos].strip()
        self.pos += 1
        if len(line) == 0:
            log.debug("Blank line")
            return (Tag.blank, "")
        tag, _, body = line.partition(":")
        log.debug("Split line into parts")
        if tag in tags:
            log.debug("Recognized a tag")
            # Including any following lines that don't
            # start with a marker
            while (len(self.lines[self.pos].strip()) > 0 and
                       self.lines[self.pos].partition(":")[1] == ""):
                body += " " + self.lines[self.pos].strip()
                self.pos += 1
            return (Tag(tag), body)
        log.debug("Confused")
        return (Tag.ERROR, line)



def convert(lines: List[str]) -> List[str]:
    """Input is the lines of the file, in list form so that
    we can flexibly traverse them.
    Form of output as dicts/lists:
    {  title: text,
       author: text,
       book: text,
       year: text,
       translator: text,
       verse: list of
           lines: list of
               list of (original: text, translated: text)
    """
    log.debug("Convert called")
    at_break = True
    result = { "title": "No title provided",
               "author": "Author not specified",
               "translator": "Translator not specified",
               "verse": []
               }
    lnum = 0

    while (lnum < len(lines)):
        log.debug(f"Processing line {lines[lnum]}")
        line = lines[lnum].strip()

        if len(line) == 0:
            log.debug("Skipping")
            lnum += 1
            continue

        if line.startswith("title:"):
            log.debug("title:")
            result["title"] = line[6:]
            lnum += 1
            continue



        if len(line) == 0:
            log.debug("Blank line")
            # Blank line after stripping
            if not at_break:
                log.debug("Stanza break")
                at_break = True
            lnum += 1
            continue

        at_break = False


        if line.startswith("o:"):
            log.debug("o:")
            tr_line = lines[lnum+1].strip()
            result["verse"].append(chunkify(line, tr_line))
            lnum += 2
            continue

        log.debug(f"Appending line {line}")
        result["verse"].append(line)
        lnum += 1

    log.debug(f"Returning {result}")
    return result

def chunkify(original: str, translation: str) -> str:
    assert original.startswith("o:")
    if not translation.startswith("t:"):
        print(f"Expecting line '{original[:15]}...' to be followed by translation line",
              file=sys.stderr)
        return

    or_chunks = original[3:].split("|")
    tr_chunks = translation[3:].split("|")
    if len(or_chunks) != len(tr_chunks):
        print(f"{len(or_chunks)} chunks in '{original[:15]}...' not matched by " +
              f"{len(tr_chunks)} in '{translation[:15]}...'")
        return

    result = []
    for chunk_i in range(len(or_chunks)):
        result.append('<div class="chunk">')
        result.append(f'\t<div class="es">{or_chunks[chunk_i]}</div>')
        result.append(f'\t<div class="en hide">{tr_chunks[chunk_i]}</div>')
        result.append('</div> <!-- chunk -->')

    return '\n'.join(result)

# Just for testing
if __name__ == "__main__":
    example = open("data/nada_mas.txt").readlines()
    #converted = convert(example)
    #for line in converted:
    #   print(line)
    lexer = Lexer(example)
    token, body = lexer.next()
    while token != Tag.EOF:
        print(f"{token.name}: {body}")
        token, body = lexer.next()
