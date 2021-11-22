import time
from random import randint
from termcolor import colored, cprint

#Die class - to roll a single die
class Die:
    def __init__(self):
        self._value = self.roll()

    def get_value(self):
        return self._value

    def roll(self):
        self._value = randint(1, 6)  

#DiceCup class - to throw die and also bank a die
class DiceCup(Die):
    def __init__(self):
        dice = []
        banked = [0] * 5
        for i in range(5): dice.append(Die())
        dice = dict(zip(dice, banked))
        self._dice = [[key, val] for key, val in dice.items()]

    #Get value of dice
    def value(self, index):    
        return self._dice[index-1][0].get_value()

    #Banking the dice
    def bank(self, index):
        self._dice[index-1][1] = 1

    #To check is the dice banked or not
    def is_banked(self, index):
        return True if self._dice[index-1][1] == 1 else False

    #Release/erase value and initialize it to zero
    def release(self, index):
        self._dice[index-1][1] = 0
        self._dice[index-1][0]._value = 0    

    #Release all dice values
    def release_all(self):
        for i in self._dice:
            i[1] = 0
            i[0]._value = 0

    # rolls the die which are not banked
    def roll(self):
        r = 1
        for i in self._dice:
            if (not self.is_banked(r)): i[0].roll()
            r = r + 1

#ShipOfFoolsGame class - For 1 round of Person's Game
class ShipOfFoolsGame(DiceCup):
    def __init__(self):
        self._cup = DiceCup()
        self.winning_score = 21

    def round(self):
        #round number
        self.roundnum = 1  
        has_ship = False
        has_captain = False
        has_crew = False

        #count of die going to be thrown
        num = 5    
        #number of die which are banked 
        banked = 0  
        #final score
        final = 0
        
        while(self.roundnum <= 3):
            cprint('\n****************************', 'red')
            cprint('\nRolling Dice ...... ', 'green')
            time.sleep(2)
            print("\nDice Roll: ", self.roundnum)
            print("Number of dice: ", num)
            print("Banked dice: ", banked)
            
            #roll dice
            self._cup.roll() 

            #store dice value for that roll
            dices = []   

            #store score in that round
            score = 0
            p = False
            q = False

            #Print Dice Values
            print("Dice values:")
            for i in range(1, len(self._cup._dice)+1):
                if(not self._cup.is_banked(i)): print(self._cup.value(i), end=" ")
            print()

            #check ship is present or not
            for i in range(1, len(self._cup._dice)+1):
                if (self._cup.value(i) == 6 and not has_ship):
                    has_ship = True
                    self._cup.bank(i)
                    print("6 banked")
                    p = True
                    banked = banked + 1
                    num = num - 1
                    break

            #check captain is present or not
            for i in range(1, len(self._cup._dice) + 1):
                if (self._cup.value(i) == 5 and has_ship and not has_captain):
                    has_captain = True
                    self._cup.bank(i)
                    print("5 banked")
                    p = True
                    banked = banked + 1
                    num = num - 1
                    break

            #check crew is present or not
            for i in range(1, len(self._cup._dice)+1):
                if (self._cup.value(i) == 4 and not has_crew and has_ship and has_captain):
                    has_crew = True
                    self._cup.bank(i)
                    print("4 banked")
                    p = True
                    banked = banked + 1
                    num = num - 1
                    break

            #store dice values which are not banked
            for i in range(1, len(self._cup._dice) + 1):
                if(not self._cup.is_banked(i)):
                    dices.append(self._cup.value(i))
                    score = score + self._cup.value(i)
                    #if any die is banked print unbanked die
                    if(p):    
                        print("Remaining dice values: ")
                        q = True
                        p = False
                    if(q): print(self._cup.value(i), end=" ")
            print()

            #If we have ship,captain,crew
            if(has_ship == has_captain == has_crew == True):
                #If it was first round or second round and we have two die
                if((self.roundnum == 1 or self.roundnum == 2) and len(dices) == 2):
                    print("Are you willing to sustain:\n1. both values\n2. single value\n3. none")
                    ans = int(input())
                    #to sustain both values
                    if(ans == 1):        
                        print("Values: ", dices)
                        final = score
                        self._cup.release_all()
                        return final
                    #to sustain a single value
                    elif(ans == 2):      
                        print("Choose one to sustain:", dices)
                        val = int(input())
                        final = final + val
                        #banking the die selected
                        for id in range(1, len(self._cup._dice)+1):  
                            if (self._cup.value(i) == val and not self._cup.is_banked(i)):
                                self._cup.bank(i)
                                banked = banked + 1 
                                num = num - 1
                                break
                        self.roundnum = self.roundnum + 1
                    #to discard both values    
                    elif(ans == 3): self.roundnum = self.roundnum + 1
                #one dice in second round
                elif((self.roundnum == 2) and len(dices) == 1):
                    ans = input("Like to sustain it(Y/N): ")

                    if(ans == 'Y' or ans == 'y'):
                        x = final
                        final = score + final
                        print("The values are: ", x, score)
                        self._cup.release_all()
                        return final

                    elif(ans == 'N' or ans == 'n'):
                        self.roundnum = self.roundnum + 1

                #die in third round
                elif(self.roundnum == 3):
                    #only one dice
                    if(len(dices) == 1):
                        x = final
                        final = final + score
                        print("The values are:", x, score)
                        self._cup.release_all()
                        return final
                    #two dice
                    elif(len(dices) == 2):     
                        print("Values: ", dices)
                        self._cup.release_all()
                        final = score
                        return final
            #There is either ship or captain or crew or there is no ship no captain no crew
            elif((has_ship == True or has_captain == True or has_crew == True)or(has_ship == has_captain == has_crew == False)):
                self.roundnum = self.roundnum + 1

            if(self.roundnum == 4):
                cprint("Ship Captain Crew not occurred in order", 'red')
                self._cup.release_all()
                return 0

#Player class - To Player Round
class Player:
    def __init__(self, name="", score=0):
        self._name = name
        self._score = score

    #to set the name
    def set_name(self, name):
        self._name = name

    #to return the current score
    def current_score(self):
        return self._score

    #to reset the score
    def reset_score(self): 
        has_ship = False
        has_captain = False
        has_crew = False
        crew = 0
        self._score = 0

    #player round
    def play_round(self, obj):   
        self._score = self._score + obj.round()      

#PlayRoom class - rounds for all players
class PlayRoom(ShipOfFoolsGame, Player):
    def __init__(self):
        self._game = None
        self._players = []

    #to set the game
    def set_game(self):
        self._game = ShipOfFoolsGame()

    #to add a player
    def add_player(self, Player):
        self._players.append(Player)

    #to reset the scores
    def reset_scores(self):
        self.has_ship = False
        self.has_captain = False
        self.has_crew = False
        self.crew = 0
        for p in self._players:
            p.reset_score()

    #rounds of all the players
    def play_round(self):
        r = 1
        while(not self.game_finished()):
            for p in self._players:
                print("Round: ", r, " Player:", p._name, end=" ")
                p.play_round(self._game)
                print("Current score of", p._name, "is", p.current_score(), end="\n\n")
            r = r + 1

    #check game finished or not
    def game_finished(self):    
        for p in self._players:
            if(p.current_score() >= self._game.winning_score):
                return True
        return False

    #display scores of players
    def print_scores(self):    
        for p in self._players:
            print(p._name, "final score is", p.current_score())

    #Show winner
    def print_winner(self):   
        maxp = 0
        n = ""
        for p in self._players:
            if(p.current_score() >= self._game.winning_score and p.current_score() > maxp):
                maxp = p.current_score()
                n = p._name
        print("Winner is", n, "with score", maxp)

#Driver
if __name__ == "__main__":
    room = PlayRoom()
    room.set_game()
    room.add_player(Player("Suvoj"))
    room.add_player(Player("Navya"))
    room.reset_scores()
    while not room.game_finished():
        room.play_round()
        room.print_scores()
    room.print_winner()