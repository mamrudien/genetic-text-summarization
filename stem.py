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

import argparse
import sys

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

def stem(text: str) -> str:
    return stemmer.stem(text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stemming Indonesian text')

    parser.add_argument('source', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Source file.')
    parser.add_argument('destination', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Destination file.')
    
    args = parser.parse_args()
    
    for line in args.source.readlines():
        print(stem(line), file=args.destination)
