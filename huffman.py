#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

''' Huffman encoding
P(A) = 0.12
P(B) = 0.15
P(C) = 0.15
P(D) = 0.18
P(E) = 0.22
P(F) = 0.12
P(G) = 0.06

symbols = {"A":0.12, "B": 0.15, "C": 0.15, "D": 0.18, "E": 0.22, "F": 0.12, "G": 0.06}
for symbol in symbols:
    print "symbol= %s; P(%s)= %0.4f" % (symbol, symbol, symbols[symbol])
symbols = ["A", "B", "C", "D", "E", "F", "G"]
probabilities = [0.12, 0.15, 0.15, 0.18, 0.22, 0.12, 0.02]
'''

class Node:
    # properties
    probability = 0.0
    symbol = ""
    encoding = ""
    visited = False
    parent = -1

class Huffman:
    Tree = None
    Root = None
    Nodes = []
    probs = {}
    dictEncoder = {}
    
    # methods
    def __init__(self, symbols):
        self.initNodes(symbols)
        self.buildTree()
        self.buildDictionary()

    def initNodes(self, probs):
        for symbol in probs:
            node = Node()
            node.symbol = symbol 
            node.probability = probs[symbol]
            node.visited = False
            self.Nodes.append(node)
            self.probs[symbol]=probs[symbol]           

    def showTree(self):
        print "--------------------------"
        for i in range(0, len(self.Nodes)):
            symbol = self.Nodes[i].symbol
            prob = self.Nodes[i].probability
            visited = self.Nodes[i].visited
            parent = self.Nodes[i].parent
            encoding = self.Nodes[i].encoding
            print "[%d] Symbol= %s, Prob(%s) = %0.4f, visited=%d; parent=%d; enc=%s" % (i, symbol, symbol, prob, visited, parent, encoding)

    def buildTree(self):
        indexMin1 = self.getNodeWithMinimumProb()
        indexMin2 = self.getNodeWithMinimumProb()
        
        while indexMin1 != -1 and indexMin2 != -1:
            node = Node()
            node.symbol = "."
            node.encoding = ""
            prob1 = self.Nodes[indexMin1].probability
            prob2 = self.Nodes[indexMin2].probability
            node.probability = prob1 + prob2
            node.visited = False
            node.parent = -1
            self.Nodes.append(node)
            self.Nodes[indexMin1].parent = len(self.Nodes) - 1
            self.Nodes[indexMin2].parent = len(self.Nodes) - 1
            
            # rule: 0 to highest probability, 1 to lowest.
            if prob1 >= prob2:
                self.Nodes[indexMin1].encoding = "0"
                self.Nodes[indexMin2].encoding = "1"
            else:
                self.Nodes[indexMin1].encoding = "1"
                self.Nodes[indexMin2].encoding = "0"
            
            # self.showTree()
            
            indexMin1 = self.getNodeWithMinimumProb()
            indexMin2 = self.getNodeWithMinimumProb()

    def getNodeWithMinimumProb(self):
        minProb = 1.0
        indexMin = -1

        for index in range(0, len(self.Nodes)):
            if (self.Nodes[index].probability < minProb  and 
               (not self.Nodes[index].visited)):
                minProb = self.Nodes[index].probability
                indexMin = index

        if indexMin != -1:
            self.Nodes[indexMin].visited = True

        return indexMin
   
    def showSymbolEncoding(self, symbol):
        found = False
        index = 0
        encoding = ""

        for i  in range(0, len(self.Nodes)):
            if self.Nodes[i].symbol == symbol:
                found = True
                index = i
                break 
        
        if found:
            while index != -1:
                encoding = "%s%s" % (self.Nodes[index].encoding, encoding)      
                index = self.Nodes[index].parent
        else:
            encoding = "Unknown symbol"

        return encoding

    def buildDictionary(self):
        for symbol in self.probs:
            encoding = self.showSymbolEncoding(symbol)
            self.dictEncoder[symbol] = encoding
                
    def encode(self, plain):
        encoded = ""
        for symbol in plain:
            encoded = "%s%s" % (encoded, self.dictEncoder[symbol])

        return encoded 

    def decode(self, encoded):
        index = 0
        decoded = ""

        while index < len(encoded):
            founf = False
            aux = encoded[index:]
            for symbol in self.probs:
                if aux.startswith(self.dictEncoder[symbol]):
                    decoded = "%s%s" % (decoded, symbol)
                    index = index + len(self.dictEncoder[symbol])
                    break 
        
        return decoded



if __name__=="__main__":
    # symbols,probabilities table
    symbols = {"A":0.12, "B": 0.15, "C": 0.15, "D": 0.18, "E": 0.22, "F": 0.12, "G": 0.06}

    # instantiate encoder
    huffman = Huffman(symbols)
     
    print "show symbols"
    for symbol in symbols:
        print "Symbol: %s; encoding: %s" % (symbol, huffman.showSymbolEncoding(symbol))

    test = "ABABCCFDADDEDAG"
    encoded = huffman.encode(test)
    print "test: %s; encoded: %s" % (test, encoded)
    decoded = huffman.decode(encoded)
    print "encoded: %s; decoded: %s" % (encoded, decoded)

    if test == decoded:
        print "Success!"
