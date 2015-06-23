##!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import json
import csv
import string
import codecs
import itertools
from collections import namedtuple
from operator import itemgetter
import numpy as np
import nltk
from gensim.models import word2vec

#from sklearn.decomposition import PCA
#from sklearn.manifold import TSNE
from tsne import bh_sne

def load_list_of_frequent_words( word_freq_filename ):
    FWord = namedtuple('FWord', 'rank,word,count,whatever')
      
    frequent_words = set()

    for line in csv.reader(open( word_freq_filename, "rb"), delimiter=str(",")):
        
        if len( line ) == 4:
            record = FWord._make(line)

            rank, word, count, _ = record

            frequent_words.add( unicode(word.lower(), "utf-8") )

    return frequent_words

def parse_file( filename, model, frequent_words, other_word_vectors=None, other_word_labels_set=None, NUM_OF_OUTPUT_WORDS=750 ):
    word_vectors = {}
    intersection_word_vectors = {}

    f = codecs.open( filename, encoding='utf-8' )
    for line in f:
        line = line.lower()
        line = " ".join("".join([" " if ch in string.punctuation else ch for ch in line]).split())

        words = nltk.word_tokenize( line )

        for word in words:
            if not word in frequent_words:
                if word in model:
                    if word not in word_vectors:
                        word_vectors[ word ] = [ 1, model[ word ] ]

                        if other_word_vectors:
                            if word in other_word_labels_set:
                                if word not in intersection_word_vectors:
                                    intersection_word_vectors[ word ] = [ 1, model[ word ] ]
                                else:
                                    intersection_word_vectors[ word ][ 0 ] += 1
                    else:
                        word_vectors[ word ][ 0 ] += 1

                        if other_word_vectors:
                            if word in other_word_labels_set:
                                if word not in intersection_word_vectors:
                                    intersection_word_vectors[ word ] = [ 1, model[ word ] ]
                                else:
                                    intersection_word_vectors[ word ][ 0 ] += 1

    # compute word list with NUM_OF_OUTPUT_WORDS most frequent words
    word_vectors_list = []
    for key, value in word_vectors.iteritems():
        temp = [key,value]

        word_vectors_list.append( [value[0], key, value[1]]  )
    word_vectors_list = sorted(word_vectors_list, key=lambda w: w[0], reverse=True)[0:NUM_OF_OUTPUT_WORDS]

    # compute intersection list with NUM_OF_OUTPUT_WORDS most frequent words
    intersection_word_vectors_list = []
    if other_word_vectors:
        for key, value in intersection_word_vectors.iteritems():
            temp = [key,value]

            intersection_word_vectors_list.append( [value[0], key, value[1]]  )
        intersection_word_vectors_list = sorted(intersection_word_vectors_list, key=lambda w: w[0], reverse=True)[0:NUM_OF_OUTPUT_WORDS]

    return word_vectors_list, set( word_vectors.keys() ), intersection_word_vectors_list

def collect_vectors_labels_and_counts( parsed_vectors ):
    vectors = []
    labels = []
    counts = []

    for i in xrange( len(parsed_vectors ) ):
        counts.append( parsed_vectors[ i ][ 0 ] )
        labels.append( parsed_vectors[ i ][ 1 ] )
        vectors.append( parsed_vectors[ i ][ 2 ] )

    return vectors, labels, counts

def remove_intersection_set_from_list( word_vectors_x, word_labels_x, word_counts_x, intersection_set ):

    for i in xrange( len( word_vectors_x ) - 1,-1,-1 ):
        if word_labels_x[ i ] in intersection_set:
            del word_vectors_x[ i ]
            del word_labels_x[ i ]
            del word_counts_x[ i ]
    return word_vectors_x, word_labels_x, word_counts_x

def do_tsne_on_vectors_and_write_json( word_vectors_a, word_labels_a, word_counts_a, 
        word_vectors_b, word_labels_b, word_counts_b, 
        word_vectors_i, word_labels_i, word_counts_i ):

    # flatten
    vectors = list( itertools.chain.from_iterable( [ word_vectors_a, word_vectors_b, word_vectors_i ] ) )
    vectors = np.asfarray( vectors, dtype='float' )

    idx_a = len( word_vectors_a )
    idx_b = len( word_vectors_b )
    idx_i = len( word_vectors_i )

    tsne_vectors = bh_sne( vectors )
    tsne_vectors *= 10000

    output_for_json = {}

    output_for_json[ "topics_a" ] = render_json( tsne_vectors[:idx_a], word_labels_a, word_counts_a )
    output_for_json[ "topics_b" ] = render_json( tsne_vectors[idx_a:idx_a+idx_b], word_labels_b, word_counts_b )
    output_for_json[ "topics_i" ] = render_json( tsne_vectors[idx_a+idx_b:], word_labels_i, word_counts_i )

    print json.dumps( output_for_json )
    
def render_json( vectors, labels, counts ):
    output_for_json = []

    vectors = np.array( vectors )

    for i in range( len( vectors ) ):
        new_hash = {}

        new_hash["title"] = str(labels[ i ])
        new_hash["x"] = int(vectors[ i ][ 0 ])
        new_hash["y"] = int(vectors[ i ][ 1 ])
        new_hash["size"] = int( counts[ i ] )

        output_for_json.append( new_hash )
 
    return output_for_json

try:    
    DATA_BASE_PATH = "REPLACE_WITH_RELATIVE_PATH"
    filename_source_a = DATA_BASE_PATH + "REPLACE_WITH_FILENAME_A"
    filename_source_b = DATA_BASE_PATH + "REPLACE_WITH_FILENAME_B"

    # load word vectors
    word2vec_vectors_filename = "vectors.bin"
    model = word2vec.Word2Vec.load_word2vec_format( word2vec_vectors_filename, binary=True )

    # load most frequent words
    word_freq_filename = "word_freq.csv"
    frequent_words = load_list_of_frequent_words( word_freq_filename )

    # parse file and collect intersection vectors
    word_vectors_list_a, word_labels_set_a, _ = parse_file( filename_source_a, model, frequent_words )
    word_vectors_list_b, word_labels_set_b, word_vectors_list_i = parse_file( filename_source_b, model, frequent_words, word_vectors_list_a, word_labels_set_a )
    
    # split the parsed input
    word_vectors_a, word_labels_a, word_counts_a = collect_vectors_labels_and_counts( word_vectors_list_a ) 
    word_vectors_b, word_labels_b, word_counts_b = collect_vectors_labels_and_counts( word_vectors_list_b ) 
    word_vectors_i, word_labels_i, word_counts_i = collect_vectors_labels_and_counts( word_vectors_list_i ) 

    # find intersection set
    word_labels_set_i = set( map(itemgetter(1), word_vectors_list_i ) )

    # remove the intersection set vectors from a and b
    word_vectors_a, word_labels_a, word_counts_a = remove_intersection_set_from_list( word_vectors_a, word_labels_a, word_counts_a, word_labels_set_i )
    word_vectors_b, word_labels_b, word_counts_b = remove_intersection_set_from_list( word_vectors_b, word_labels_b, word_counts_b, word_labels_set_i )

    do_tsne_on_vectors_and_write_json( word_vectors_a, word_labels_a, word_counts_a, word_vectors_b, word_labels_b, word_counts_b,  word_vectors_i, word_labels_i, word_counts_i )

except Exception, e:
    print "Couldn't process files"
    print "Exception:", e
    raise
    sys.exit(1)
