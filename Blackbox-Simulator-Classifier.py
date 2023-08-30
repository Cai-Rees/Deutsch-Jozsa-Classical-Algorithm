#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This code solves the Deutsch-Jozsa problem classically. 

----
The Deutsch-Jozsa problem involves classifying a black box. The blackbox takes 
a n-bit sequence and returns a single bit. The blackbox is one of the following types:

Balanced: For half the input space the black box returns an output of 0 and for 
the other half has an output of 1

Constant: For all the input space returns either a 1 or 0
-----
This code aims to reproduce the case of general black box that could have
any form of mapping from the input to output space. When classifying the black box the number of operations
used to classify it is always the minimum possible. 

The code uses intergers as representative of unique bitstring to facilitate 
operations with them. The code plots the average number of outputs scales 
with bits in the bitstring. There is also a commented section at the end which
plots a histogram of the number of operations needed to classify a black box that 
takes a specified length of bitstring 


Author: Cai Rees 5/03/2023

"""

import numpy as np
import random
import matplotlib.pyplot as plt

class general_black_box:
    """
    A class used to represent a black box takes bitstring inputs and maps them to binary outputs.
    Its two possible types are 
    balanced - half the input space maps to 0, the other half to 1
    constant - all mapings are to 0 or 1
    
    Attributes
    ----------
    type : int
        indicates the type of the black box, 0: constant, 1: balanced.
    input_bitstring_length : int
        number of bits in bitstring black box takes as input.
    output: int
        output in the constant type case
    output_array : numpy array
        outputs in the balanced type case

    Methods
    -------
    input_output_operation(bit_string_input: int)
        takes input and returns corresponding binary output
    """
    def __init__(self, black_box_type, black_box_bit_string_length):
        # type indicated by boolean. 0: constant, 1: balanced.
        self.type = black_box_type 
        
        #initialise the length of bitstring blackbox takes
        self.input_bitstring_length = black_box_bit_string_length 
        
        # determine the outputs depending which type black box was initiliase with
        if self.type == 0:
            # output is fixed on either 0 or 1
            self.output = np.random.choice([0, 1])
        
        else:
            # calculate the number of unique bitstrings
            number_of_possible_bitsrtings = int(2 ** self.input_bitstring_length)
            # create an equal number of 0 or 1 outputs 
            temp_zero_array = np.zeros(int(number_of_possible_bitsrtings / 2), dtype=int)
            temp_ones_array = np.ones(int(number_of_possible_bitsrtings / 2), dtype=int)
            # join them in an array and shuffle their order
            black_box_output_array = np.concatenate((temp_zero_array, temp_ones_array))
            random.shuffle(black_box_output_array)
            # this array now holds an equal number of 0 and 1 outputs 
            # this simulates any general mapping function that could be used by a black box
            self.output_array = black_box_output_array
            
    def input_output_operation(self, bit_string_input):
        # returns the corresponding output to the binary representation of a bitstring 
        # in the case that the blackbox is of constant type then return its fixed output
        # validation has been ommitted to check if bit_string_input is in valid range
        # the functions which use this method use".input_bitstring_length" to ensure range is not exceeded
        if self.type == 0:
            bit_string_output = self.output
        else:
            # the input is mapped to a unique output of 0 or 1 by interpreting it as an index
            bit_string_output = self.output_array[bit_string_input]
        return bit_string_output

def black_box_classifier(black_box):
    """
    Takes a black box and by passing bitstrings through the black box and comparing outputs 
    determines if the black box is of a constant or balanced type.  
    
    Args:
        black_box(general_black_box): Object of custom class

    Returns:
        black_box_type (boolean): binary classifiaction of black box. 
        number_of_black_box_outputs (int): Number of input output passes required for classification.
    
    """
    # compute the maximum number of values able to be represented in the input bit string
    number_of_possible_bitsrtings = 2 ** black_box.input_bitstring_length
    
    # begin with assumption that the black box of a "constant type" - 0 represents constant
    black_box_type = 0
    
    # create a list of intergers each representative of a unique bitstring in binary
    # intergers shuffled so that on average solver requires same number of operations for any black box
    black_box_input_list = [i for i in range(number_of_possible_bitsrtings)]
    random.shuffle(black_box_input_list)

    # iterate through list, bounded by minimum operations needed to say box is constant
    # note that the first operation outside the loop counts towards this total 
    black_box_output_1 = black_box.input_output_operation(black_box_input_list[0])
    for counter in range(int(number_of_possible_bitsrtings / 2)):
        
        # at each stage compute the binary output of the subsequent bitstring
        black_box_output_2 = black_box.input_output_operation(black_box_input_list[counter+1])
        
        # classify black box as balanced in the case that two outputs are different and exit loop
        if black_box_output_1 != black_box_output_2:
            black_box_type += 1
            break
        black_box_output_1 = black_box_output_2
            
    # calculate the number of times a blackbox output was computed 
    number_of_black_box_outputs = counter + 2
    
    return black_box_type, number_of_black_box_outputs

def test_black_box_classifier(length_of_bitstring, number_of_tests):
    """
    Simulates a blackbox of balanced or constant type with equal probability. Classifies this blackbox and 
    records its type and how many operations were required to classsify it. 
    
    Args:
        length_of_bitstring (int):
            number of bits in bitstring input
        number_of_tests (int):
            number of repeated tests of the blackbox classifier

    Returns:
        number_of_outputs_list (list (int)): 
            A list of the number of outputs required to classify black box for every test 
        black_box_type_list (list (int)): 
            list of classifications of the black box types 
    
    """
    black_box_1 = general_black_box(1, length_of_bitstring) # initialise a balanced black box 
    black_box_2 = general_black_box(0, length_of_bitstring) # initiliase a constant black box
    
    # empty lists to contain info from each test
    number_of_outputs_list = []
    black_box_type_list = []
    
    # test the black box classifier multiple times
    for i in range(number_of_tests):
        # randomly choose a balanced or constant black box
        black_box_in_use = random.choice([black_box_1, black_box_2])
        
        # classify black box
        black_box_type, number_of_black_box_outputs = black_box_classifier(black_box_in_use)
        number_of_outputs_list.append(number_of_black_box_outputs)
        black_box_type_list.append(black_box_type)
        
        # ensure classification is correct
        if black_box_in_use.type != black_box_type:
            print("Black box misclassified!")
    
    return number_of_outputs_list, black_box_type_list

def average_output_number_scaling(maximum_bitstring_length, number_of_tests):
    """
    Plots the average number of outputs needed as the length of the bitstring increases
    Args:
        maximum_bitstring_length (int):
            largest number of bits in a bitstring tested
        number_of_tests (int):
            number of repeated tests of the blackbox classifier for each bitstring

    Returns:
         None
    """
    # empty list to contain the average number of operations
    average_operations_list = []
    # iterate up till the maximum bitstring length
    for i in range(maximum_bitstring_length):
        # call the black box tester
        number_of_outputs_list, black_box_type_list = test_black_box_classifier(i+1, number_of_tests)
        # compute the average number of operations required
        average_operations_list.append(np.mean(number_of_outputs_list))
    plt.plot([i+1 for i in range(maximum_bitstring_length)] , average_operations_list)
    plt.title("Average number of outputs computed for classification")
    plt.xlabel("Number of bits in bitstring")
    plt.tight_layout()
    plt.show()


number_of_trials = 50
maximum_bitstring_length_tested = 17
average_output_number_scaling(maximum_bitstring_length_tested, number_of_trials)

# commented code below plots a histogram of the number of operations needed to
# classify a black box that takes a specified length of bitstring 
"""
# test the black box classifier
bit_string_length = 10
number_of_trials = 1000
number_of_outputs_list, black_box_type_list = test_black_box_classifier(bit_string_length, number_of_trials)

fig, ax = plt.subplots(2, figsize=(30, 15))
ax[0].set_xlabel("Number of outputs computed", fontsize = 10)
ax[1].set_xlabel("Number of outputs computed", fontsize = 10)
ax[0].set_ylabel("Frequency", fontsize = 10)
ax[1].set_ylabel("Frequency - log scale", fontsize = 10)
ax[0].set_title(f"Histogram of number of required input-output passses to classify a black box that takes"
             f" bitstrings of length {bit_string_length}\n Number of trials: {number_of_trials} \n Average " 
             f"number of outputs computed: {np.mean(number_of_outputs_list) } \n" 
             f"Maximum number of outputs required: {2**(bit_string_length-1) + 1}"
             f"\n Number of unique bitstrings: {2**bit_string_length}", fontsize = 15)

ax[0].hist(number_of_outputs_list, bins=range(min(number_of_outputs_list), max(number_of_outputs_list) + 1, 1))
ax[1].hist(number_of_outputs_list, bins=range(min(number_of_outputs_list), max(number_of_outputs_list) + 1, 1), log=True)
plt.tight_layout()
plt.show()
"""
