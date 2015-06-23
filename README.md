# Topic Comparison Tool

The tool provides a bird’s-eye view of a text source. It takes a text and maps the words so that semantically and stylistically similar words are close to each other. This enables users to explore a text source like a geographical map. As similar words are close to each other, the user can visually identify clusters of topics that present in the book. Conceptually, it can be understood as a Fourier transformation for texts.

The Topic Comparison module can be used to compare a summary and its source material. To compare the topics, three different sets of words are computed: a source text topic set, a summary topic set, as well as the intersection set of both topic sets. A colour is assigned to each set of words. This enables the user to visually compare the different text sources and to see which topics are covered where. The user can explore the word map and zoom in and out. He or she can also toggle the visibility, i.e. show and hide, certain word sets.

## How it works


### Pre-processing 

In the pre-processing step, all sentences are tokenized to extract single words. The tokenization is done using the Penn Treebank Tokenizer implemented in the Natural Language Processing Toolkit (NLTK) for Python. Alternatively, this could also be achieved with a regular expression.

Using a hash map, all words are counted. Only unique words, i.e. the keys of the hash map, are taken into account for the dimensionality reduction. Not all unique words are taken into account. The 3000 most frequent English words according to a frequency list collected from Wikipedia are ignored to reduce the amount of data.

### Word representations

For all unique non-frequent words, the word representation vectors are collected from the word2vec model via the gensim Python library. Each word is represented by a N-dimensional vector (N=300).

### Dimensionality Reduction 

The results of the word2vec vectors are projected down to 2D using the t-SNE Python implementation in scikit-learn.

### Visualization

After the dimensionality reduction, the vectors are written to a JSON file. The vectors are visualized using the D3.js Javascript data visualization library. Using D3.js, an interactive map was developed. With this map, the user can move around and zoom in and out.

## Thesis

The title of the thesis is "Semantic and stylistic text analysis for book summary evaluation". It was written at KTH Royal Institute of Technology in Stockholm and Aalto University in Helsinki. The Master thesis describes the development of a tool for the text analysis of book summaries. The tool evaluates a summary and its source material in regards to topics, stories, readability, and emotionality. It visualizes the results in a dashboard.

## License

2015 Hendrik Heuer hendrikheuer@gmail.com

GNU General Public License 3

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.