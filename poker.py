import random
from collections import Counter
import pandas as pd


class deck():
    def __init__(self,n):
        self.cards = self.createdeck(n)
        self.shuffledeck()

    def createdeck(self, n):
        d = []
        for i in range(n):
            for s in range(4):
                for c in range(1,14):
                    d.append((s,c))
        return d

    def shuffledeck(self):
        random.shuffle(self.cards)

class player():
    def __init__(self):
        self.cards = []

    def reset(self):
        self.cards = []

    def checkhand(self, c):
        hand = self.cards
        hand.extend(c)
        
        f = flush(hand)
        s = straight(hand)
        k = kinds(hand)
        
        if max(k[0], f[0], s[0]) == k[0]:
            return k
        elif max(k[0], f[0], s[0]) == f[0]:
            return f
        else:
            return s


def flush(hand):
    l = Counter([x[0] for x in hand]).most_common()[0]
    if l[1] >= 5:
        s = straight([x for x in hand if x[0] == l[0]])
        if s[0] == 5:
            return [10, s[1]]
        else:
            return [6, [x[1] for x in hand if x[0] == l[0]]]
    else:
        return [0,0]
 

def straight(hand):
    ## Check ranges for straight, can use diff values but need to map diffs to acutal values to find high
    l = set([x[1] for x in hand])

    if set([1,13,12,11,10]).issubset(l):
        return [5, 14]
    for i in range(13,4,-1):
        if set(range(i, i-5,-1)).issubset(l):
            return [5, i]
        else:
            pass
    return [0,0]

def kinds(hand):
    ## Create counter of each card
    l = Counter([x[1] for x in hand]).most_common()

    ## Check if most common is 4x
    if l[0][1] == 4:
        ## Return 8 points and the remaning high card
        return [8,max(x[1] for x in hand if x[1] != l[0][0])]
    
    ## Check if most common is 3x
    if l[0][1] == 3:

        #Return fullhouse combo checking which triplet was higher
        if l[1][1] == 3:
            return [7, [max(l[0][0], l[1][0]), min(l[0][0], l[1][0])]]

        # Return fullhouse combo, checking if there is a 2nd pair
        if l[2][1] == 2:
            return [7, [l[0][0], max(l[1][0], l[2][0])]]

        # Return standard fullhouse
        if l[1][1] == 2:
            return [7, [l[0][0], l[1][0]]]

        #Return triplet with no pair
        if l[1][1] == 1:
            l_notriplet = [x[1] for x in hand if x[1] != l[0][0]]
            ##Convert Aces
            l_notriplet = [14 if x==1 else x for x in l_notriplet]
            l_notriplet.sort()

            ## Return triplet and 2 other high cards
            return [4, [l[0][0], l_notriplet[-2:]]]
        
    ## Check if most common is 2x
    if l[0][1] == 2:

        ## Check if there are 3 pairs
        if l[2][1] == 2:
            l_pairs = [l[0][0], l[1][0], l[2][0]]
            l_pairs.sort()
            pairs = l_pairs[-2:]
            l_nopairs = [x[1] for x in hand if x[1] not in pairs]
            
            return [3, pairs, max(l_nopairs)]
        
        ## Check for 2 pairs
        if l[1][1] == 2:
            pairs = [l[0][0], l[1][0]]
            l_nopairs = [x[1] for x in hand if x[1] not in pairs]

            return [3, pairs, max(l_nopairs)]

        ## Check for 1 pair
        if l[1][1] == 1:
            l_nopairs = [x[1] for x in hand if x[1] != l[0][0]]
            return [2, [l[0][0], l_nopairs[-3:]]]

    else:
        high = [x[0] for x in l]
        high.sort()
        return [1, high[-5:]]





class game():

    def __init__(self, players, decks):
        self.d = deck(decks)
        self.c = player()
        self.p = {}
        for i in range(players):
            self.p[i] = player()
        self.r = []

    def deal(self):
        card = 0
        for i in range(2):
            for k in self.p:
                self.p[k].cards.append(self.d.cards[card])
                card += 1

        self.c.cards.extend(self.d.cards[card:card+5])

    def result(self):
        hands = []
        high_score = 0
        for k in self.p:
            hands.append(self.p[k].checkhand(self.c.cards))
            high_score = max(high_score, hands[k][0])
        high_players = [1 if x[0] == high_score else 0 for x in hands]

        ## If there is only 1 winner no worries
        if sum(high_players) == 1:
            return (high_players.index(1), high_score)
        else:
            #high_players == [i for i,x in enumerate(high_players) if x == 1]
            pass

        ## Replace with checking for additional high cards
        return (high_players.index(1), high_score)

     
    def go(self, rounds):
        for i in range(rounds):
            ## Reset PLayers and deck
            for k in self.p:
                self.p[k].reset()
            self.c.reset()
            self.d.shuffledeck()

            #Deal Cards
            self.deal()
            ##Save player cards
            x = []
            for k in self.p:
                x.append(self.p[k].cards[:2])

            results = self.result()
            ##Save results
            self.r.append([x, self.c.cards, results])

    

if __name__ == '__main__':
    g = game(1,1)
    g.go(10**6)
    pd.DataFrame(g.r).to_csv("results.csv")
        
           