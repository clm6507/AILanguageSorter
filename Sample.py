from DataNode import DataNode, Language
from math import log2

class Sample:

    datanodes: list[DataNode]
    untested_attributes: set[int]

    def __init__(this, datanodes: DataNode, untested_attributes: set[int]):
        this.datanodes = datanodes
        this.untested_attributes = untested_attributes



    def addNode(this, node: DataNode):
        this.datanodes.append(node)


    #addes up all the nodes weights and then divides each node by that so that the collection of the weights adds to 1
    def normalizeWeights(this):
        totalWeight = 0
        for node in this.datanodes:
            totalWeight += node.weight

        for node in this.datanodes:
            node.weight = node.weight/float(totalWeight)

    #checks each node to if it is the wrong language(based off of the language pass in)
    #adds weights of badly classified nodes to the sample error and returns it
    def calculateSampleError(this, wrong_language: Language):
        sample_error = 0

        for node in this.datanodes:
            if(node.language == wrong_language):
                sample_error += node.weight

        return sample_error

    #loops through unused attributes and finds the one that has the most gain
    def calculateGreatestGainAtt(this)-> int:
        greatest_gain_att = -1

        gain = -1

        for att in this.untested_attributes:
            if(gain < this.calculateGain(this.datanodes, att)):
                greatest_gain_att = att

        return greatest_gain_att

    #returns a list of lists of DataNodes where it is [truelist, falselist]
    #seperates lists based on the attribute number passed in
    def sepListOnAttribute(this, parentList: list[DataNode], attributeNum: int) -> list[list[DataNode]]:
        list1: list[DataNode] = []
        list2: list[DataNode] = []
        for node in parentList:
            if(node.attribute_list[attributeNum]):
                list1.append(node)
            else:
                list2.append(node)

        listlist: list[list[DataNode]] = []
        listlist.append(list1)
        listlist.append(list2)
        return listlist

    #adds up all the weights of the English nodes in the list that is passed in and returns it
    def calculateWeightedTotalEnglish(this, theList: list[DataNode]):
        totalEnglish = 0
        for node in theList:
            if(node.language == Language.ENGLISH):
                totalEnglish += node.weight
        return totalEnglish

    #adds up all the weights of the Dutch nodes in the list that is passed in and returns it
    def calculateWeightedTotalDutch(this, theList: list[DataNode]):
        totalDutch = 0
        for node in theList:
            if(node.language == Language.DUTCH):
                totalDutch += node.weight
        return totalDutch
    
    #Returns the total weight of all the nodes in the passed in list
    def calculateTotalWeight(this, theList: list[DataNode]):
        total = 0
        for node in theList:
            total += node.weight
        return total

    #uses the entropy formula to calculate the entropy of a given list
    #runs checks to ensure that there is no devision by 0 in case the list only has 1 kind of language in it
    def calculateEntropy(this, entropyList: list[DataNode]) -> float:
        total = this.calculateTotalWeight(entropyList)
        if( total == 0 ):
            return 0
        
        totalEnglish = this.calculateWeightedTotalEnglish(entropyList)
        totalDutch = this.calculateWeightedTotalDutch(entropyList)

        englishRatio = float(totalEnglish)/float(total)
        dutchRatio = float(totalDutch)/float(total)
        
        if(englishRatio == 0 or dutchRatio == 0):
            return 0

        entropy: float = (-1*englishRatio*log2(englishRatio)) - (dutchRatio*log2(dutchRatio))
        return entropy


    #using the formula for gain is returns the gain based on the list and attribute number passed in
    #runs checks to ensure no division by 0 in case the list passed in is empty
    def calculateGain(this, parentList, attributeNum) -> float:
        splitList = this.sepListOnAttribute(parentList, attributeNum)
        parentEntropy = this.calculateEntropy(parentList)
        entropy1 = this.calculateEntropy(splitList[0])
        entropy2 = this.calculateEntropy(splitList[1])

        if(len(parentList) == 0):
            ratio1 = 0
            ratio2 = 0
        else:
            ratio1 = float(len(splitList[0]))/float(len(parentList))
            ratio2 = float(len(splitList[1]))/float(len(parentList))

        gain = parentEntropy - ((entropy1 * ratio1) + (entropy2 * ratio2))
        return gain
    

    #calculates the total number of nodes that are English. It does not base it's calculations on weight
    def calculateTotalEnglish(this, theList: list[DataNode]):
        totalEnglish = 0
        for node in theList:
            if(node.language == Language.ENGLISH):
                totalEnglish += 1
        return totalEnglish
    
    #calculates the total number of nodes that are Dutch. It does not base it's calculations on weight
    def calculateTotalDutch(this, theList: list[DataNode]):
        totalDutch = 0
        for node in theList:
            if(node.language == Language.DUTCH):
                totalDutch += 1
        return totalDutch
    

    #this is for decision trees only. returns the guess about what language the sample is representing
    def makeGuess(this) -> Language:
        totalEnglish = this.calculateTotalEnglish(this.datanodes)
        totalDutch = this.calculateTotalDutch(this.datanodes)
        
        if(totalEnglish > totalDutch):
            return Language.ENGLISH
        else:
            return Language.DUTCH



    def __repr__(this) -> str:
        return str(this.datanodes)
