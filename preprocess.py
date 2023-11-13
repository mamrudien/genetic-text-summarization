#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyrigth 2023 Muhammad Amrudien.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import io
import re

import argparse

from typing import Callable, Iterable, Optional, Union

class Token:

    PATTERN = r'([A-Za-z-]+)|([].,;:?!()[{}_@#/&$%~`\'"*=+-])|([0-9]+(?:[.,][0-9]+)*?)|(\s+)'

    def __init__(self, token: str):
        self.token = token
    
    @staticmethod
    def match(text: str) -> 'Token':
        if text == '':
            return None

        match = _pattern.match(text)

        if match is None:
            raise ValueError(f'Invalid token: {text}')

        if (word := match.group(1)) is not None:
            return Word(word)
        elif (punct := match.group(2)) is not None:
            return Punctuation(punct)
        elif (number := match.group(3)) is not None:
            return Number(number)
        elif (whitespace := match.group(4)) is not None:
            return Whitespace(whitespace)

    def transform(self, func):
        return Token(func(self.token))

    def isword(self):
        return (match := _pattern.fullmatch(self.token)) is not None and match.group(1) is not None
    
    def ispunct(self):
        return (match := _pattern.fullmatch(self.token)) is not None and match.group(2) is not None
    
    def isnumber(self):
        return (match := _pattern.fullmatch(self.token)) is not None and match.group(3) is not None
    
    def iswhitespace(self):
        return (match := _pattern.fullmatch(self.token)) is not None and match.group(4) is not None
    
    def __str__(self):
        return self.token
    
    def __eq__(self, other):
        return self.token == other.token
    
    def __hash__(self):
        return hash(self.token)
    
    def __len__(self):
        return len(self.token)


_pattern = re.compile(Token.PATTERN)


class Word(Token):
        
    def __init__(self, word: str):
        super().__init__(word)

        if not self.isword():
            raise ValueError(f'Invalid word: {word}')
    
    def transform(self, func: Callable[[str], str]):
        return Word(func(self.token))

    def lower(self):
        return self.transform(lambda word: word.lower())
    
    def upper(self):
        return self.transform(lambda word: word.upper())


class Punctuation(Token):
    
    def __init__(self, punct: str):
        super().__init__(punct)

        if not self.ispunct():
            raise ValueError(f'Invalid punctuation: {punct}')
    
    def transform(self, func):
        return Punctuation(func(self.token))

    def isend(self):
        return self.token in '.?!'

class Number(Token):
    
    def __init__(self, number: str):
        super().__init__(number)

        if not self.isnumber():
            raise ValueError(f'Invalid number: {number}')
    
    def transform(self, func):
        return Number(func(self.token))

    @property
    def value(self):
        return int(self)
    
    def __int__(self):
        return int(self.token)

class Whitespace(Token):

    def __init__(self, whitespace: str):
        super().__init__(whitespace)

        if not self.iswhitespace():
            raise ValueError(f'Invalid whitespace: {whitespace}')

    def transform(self, func):
        return Whitespace(func(self.token))

class Sentence(list):
        
        def __init__(self, tokens: Optional[Iterable[Token]] = []):
            super().__init__(tokens)

        def append(self, token: Word):
            super().append(token)

        def transform(self, func: Callable[[Token], Token]):
            return Sentence(map(lambda token: func(token), self))

        def lower(self):
            return self.transform(lambda token: token.lower() if token.isword() else token)

        def upper(self):
            return self.transform(lambda token: token.upper() if token.isword() else token)
        
        def filter(self, func: Callable[[Token], bool]):
            return Sentence(filter(lambda token: func(token), self))
        
        def without_punct(self):
            return self.filter(lambda token: not token.ispunct())
        
        def without_punct_exceptend(self):
            return self.filter(lambda token: not token.ispunct() or token.isend())
        
        def without_whitespace(self):
            return self.filter(lambda token: not token.iswhitespace())
        
        def without_number(self):
            return self.filter(lambda token: not token.isnumber())
        
        def without(self, tokens: Iterable[str]):
            return self.filter(lambda token: str(token) not in tokens)

        def __str__(self):
            return ''.join(map(str, self))


class Paragraph(list):
    
        def __init__(self, sentences: Optional[Iterable[Sentence]] = []):
            super().__init__(sentences)

        def append(self, sentence: Sentence):
            super().append(sentence)
        
        def transform(self, func: Callable[[Sentence], Sentence]):
            return Paragraph(map(lambda sentence: func(sentence), self))

        def lower(self):
            return self.transform(lambda sentence: sentence.lower())

        def upper(self):
            return self.transform(lambda sentence: sentence.upper())
        
        def filter(self, func: Callable[[Sentence], bool]):
            return Paragraph(filter(lambda sentence: func(sentence), self))
    
        def without_punct(self):
            return self.transform(lambda sentence: sentence.without_punct())
        
        def without_punct_exceptend(self):
            return self.transform(lambda sentence: sentence.without_punct_exceptend())
        
        def without_whitespace(self):
            return self.transform(lambda sentence: sentence.without_whitespace())
        
        def without_number(self):
            return self.transform(lambda sentence: sentence.without_number())
        
        def without(self, tokens: Iterable[str]):
            return self.transform(lambda sentence: sentence.without(tokens))

        def __str__(self):
            return ''.join(map(str, self))


class Document(list):

    def __init__(self, document: Optional[Union[Iterable[Paragraph], str, io.IOBase]] = []):
        if isinstance(document, str):
            document = map(lambda line: self._paragraph(line), document.splitlines())
        elif isinstance(document, io.IOBase):
            document = map(lambda line: self._paragraph(line), document.readlines())

        super().__init__(document)

    def _paragraph(self, line: str) -> Paragraph:
        paragraph = Paragraph()
        sentence = Sentence()

        while token := Token.match(line):
            if token.ispunct() and token.isend():
                sentence.append(token)
                paragraph.append(sentence)
                sentence = Sentence()
            else:
                sentence.append(token)

            line = line[len(token):]
            
        return paragraph

    def append(self, paragraph: Paragraph):
        super().append(paragraph)
    
    def transform(self, func: Callable[[Paragraph], Paragraph]):
        return Document(map(lambda paragraph: func(paragraph), self))
    
    def lower(self):
        return self.transform(lambda paragraph: paragraph.lower())
    
    def upper(self):
        return self.transform(lambda paragraph: paragraph.upper())

    def readall(self):
        for paragraph in self:
            for sentence in paragraph:
                for token in sentence:
                    yield str(token)
    
    def filter(self, func: Callable[[Paragraph], bool]):
        return Document(filter(lambda paragraph: func(paragraph), self))

    def without_punct(self):
        return self.transform(lambda paragraph: paragraph.without_punct())
    
    def without_punct_exceptend(self):
        return self.transform(lambda paragraph: paragraph.without_punct_exceptend())
    
    def without_whitespace(self):
        return self.transform(lambda paragraph: paragraph.without_whitespace())
    
    def without_number(self):
        return self.transform(lambda paragraph: paragraph.without_number())
    
    def without(self, tokens: Iterable[str]):
        return self.transform(lambda paragraph: paragraph.without(tokens))

    def __str__(self):
        return '\n\n'.join(map(str, self))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess text document.')

    parser.add_argument('source', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Input file.')
    parser.add_argument('destination', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Output file.')
    parser.add_argument('-l', '--lower', action='store_true', help='Convert text to lowercase.')
    parser.add_argument('-u', '--upper', action='store_true', help='Convert text to uppercase.')
    parser.add_argument('-p', '--without-punct', action='store_true', help='Remove punctuations.')
    parser.add_argument('-w', '--without-whitespace', action='store_true', help='Remove whitespaces.')
    parser.add_argument('-n', '--without-number', action='store_true', help='Remove numbers.')
    parser.add_argument('-x', '--without', nargs='+', help='Remove specified tokens.')

    args = parser.parse_args()

    doc = Document(args.source)

    if args.lower:
        doc = doc.lower()
    elif args.upper:
        doc = doc.upper()

    if args.without_punct:
        doc = doc.without_punct()
    if args.without_whitespace:
        doc = doc.without_whitespace()
    if args.without_number:
        doc = doc.without_number()
    if args.without:
        doc = doc.without(args.without)

    print(doc, file=args.destination)
