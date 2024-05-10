from Sample import Sample
from DataNode import DataNode, Language
from copy import deepcopy
from math import log, exp
from random import random

class TreeNode:

    #shared attributes of decision_trees and adaboost stumps
    split_on: int
    sample: Sample
    untested_attributes: set[int]

    #for decision trees
    true_node = None
    false_node = None
    is_leaf: bool

    #for adaboost stumps
    adaTrue: Sample
    adaFalse: Sample
    stumpWeight: float




    #makes a decision tree node or adaboost stump based on whether there was an untested_attributes set passed in
    def __init__(this, sample: Sample, untested_attributes: set[int] = None):
        this.sample = sample
        this.untested_attributes = untested_attributes

        if(untested_attributes != None):            
            this.true_node: TreeNode = None
            this.false_node: TreeNode = None

            this.makeChildren()
        else:
            new_untested_attributes = deepcopy(this.sample.untested_attributes)
            this.untested_attributes = new_untested_attributes
            this.makeStump()
        

    #calculates the best attribute and makes a stump for adaboost based on that
    def makeStump(this):
        best_att = this.sample.calculateGreatestGainAtt()
        split_list = this.sample.sepListOnAttribute(this.sample.datanodes, best_att)
        new_untested_attributes_1 = deepcopy(this.untested_attributes)
        new_untested_attributes_1.remove(best_att)
        new_untested_attributes_2 = deepcopy(this.untested_attributes)
        new_untested_attributes_2.remove(best_att)
        this.adaTrue = Sample(split_list[0], new_untested_attributes_1)
        this.adaFalse = Sample(split_list[1], new_untested_attributes_2)

        this.split_on = best_att

        this.stumpWeight = this.calculateStumpWeight()
        
    
    #calculates the amount say a stump has in the final decision
    def calculateStumpWeight(this):
        total_error = this.adaTrue.calculateSampleError(Language.DUTCH) + this.adaFalse.calculateSampleError(Language.ENGLISH)
        amount_of_say = (1.0/2.0)*log((1-total_error)/total_error)
        return amount_of_say


    #returns a new sample that has updated weights based on the amount of say the current stump has
    def refactorSampleWeights(this) -> Sample:
        new_sample = deepcopy(this.sample)
        for node in new_sample.datanodes:
            if(node.attribute_list[this.split_on]):
                if(node.language == Language.DUTCH):
                    node.weight*exp(this.stumpWeight)
                else:
                    node.weight*exp(-1 * this.stumpWeight)
            else:
                if(node.language == Language.ENGLISH):
                    node.weight*exp(this.stumpWeight)
                else:
                    node.weight*exp(-1 * this.stumpWeight)

        new_sample.normalizeWeights()

        return new_sample


    #takes the current sample and makes a new one of the same size based on updated weights of the current sample
    #randomly generates this new sample
    def makeNewSample(this) -> Sample:
        new_weighted_sample = this.refactorSampleWeights()

        new_datanodes: list[DataNode] = []

        #the choosing of the new sample
        
        for i in range(len(this.sample.datanodes)):
            #chooses and random number between 0 and 1
            rand_num: float = random()
            weight_total = 0

            #keeps adding to the total weight until the next node would put the total weight over the random number
            #adds that chosen node to the new sample list
            for node in new_weighted_sample.datanodes:
                if((weight_total + node.weight) > rand_num):
                    new_datanodes.append(deepcopy(node))
                    break
                else:
                    weight_total += node.weight
        
        new_untested_attributes = deepcopy(this.untested_attributes)
        new_untested_attributes.remove(this.split_on)
        return Sample(new_datanodes, new_untested_attributes)
    



    #recursively makes the entire decision tree when called
    def makeChildren(this):
        if(len(this.untested_attributes) == 0):
            this.is_leaf = True
            this.split_on = None
            thing = len(this.sample.datanodes)

            #print(str(this.sample.calculateTotalEnglish(this.sample.datanodes)) + ",", str(this.sample.calculateTotalDutch(this.sample.datanodes)))
            
            #if(thing == 100):
            #    print(this.sample.datanodes[0].data_string)
        else:
            this.is_leaf = False

            best_att = this.sample.calculateGreatestGainAtt()
            this.split_on = best_att
            split_list = this.sample.sepListOnAttribute(this.sample.datanodes, best_att)

            empty_list1 = []
            empty_list2 = []
            cpy_set1 = set()
            cpy_set2 = set()
            for att in this.untested_attributes:
                if(att != best_att):
                    cpy_set1.add(att)
                    cpy_set2.add(att)
            cpy_sample1: Sample = Sample(empty_list1, cpy_set1)
            cpy_sample2: Sample = Sample(empty_list2, cpy_set2)

            for datanode in split_list[0]:
                cpy_sample1.addNode(deepcopy(datanode))

            for datanode in split_list[1]:
                cpy_sample2.addNode(deepcopy(datanode))


            cpy_set1 = set()
            cpy_set2 = set()
            for att in this.untested_attributes:
                if(att != best_att):
                    cpy_set1.add(att)
                    cpy_set2.add(att)

            this.true_node = TreeNode(cpy_sample1, cpy_set1)
            this.false_node = TreeNode(cpy_sample2, cpy_set2)

            #if(len(this.sample.datanodes)):
                #print(this.split_on)
            
        

    #FOR DECISION TREES ONLY
    #makes a guess about the passed in DataNode based on the current decision tree
    #makes this guess recusively
    def makeGuess(this, datanode: DataNode) -> Language:
        if(this.is_leaf):
            return this.sample.makeGuess()
        else:
            if(datanode.attribute_list[this.split_on]):
                return this.true_node.makeGuess(datanode)
            else:
                return this.false_node.makeGuess(datanode)
            

    def __repr__(this) -> str:
        if( this.untested_attributes == None):
            pass
        else:
            if(this.is_leaf):
                return str(this.sample.makeGuess())
            else:
                return "(" + str(this.true_node) + "<-" + this.split_on + "->" + str(this.false_node) + ")"
        
