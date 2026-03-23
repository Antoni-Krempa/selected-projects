import copy
import random

class Hat:
    def __init__(self,**kwargs):

        # self.contents = []
        # for i in kwargs.keys():
        #     for j in range(kwargs.get(i)):
        #         self.contents.append(i)

        self.contents = [i for i in kwargs.keys() for j in range(kwargs.get(i)) ]

    def draw(self,number_to_draw):
        number_in_hat = len(self.contents)
        

        if number_to_draw > number_in_hat:
            kule = self.contents
            self.contents = []
            return kule
        else:
            random_numbers = random.sample(range(0, number_in_hat), number_to_draw)

            list1 = []
            remove = []
            for i in random_numbers:
                list1.append(self.contents[i])
                remove.append(i)
            tab = self.contents
            self.contents = [tab[i] for i in range(number_in_hat) if i not in remove]
            
            return list1
    

    def __str__(self):
        string = ''
        # for idx, k in enumerate(self.contents):
        #     string += f'kula {idx}: {k}\n'

        return str(self.contents)

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    pass


hat1 = Hat(yellow=3, blue=2, green=6)
hat2 = Hat(red=5, orange=4)
hat3 = Hat(red=5, orange=4, black=1, blue=0, pink=2, striped=9)

print(hat1)

print(hat1.draw(6))

def experiment(hat,expected_balls,num_balls_drawn,num_experiments):
    M = 0
    expected_balls = [i for i in expected_balls.keys() for j in range(expected_balls.get(i)) ]
    hat_changing = copy.deepcopy(hat)
    for i in range(num_experiments):
        draw = hat_changing.draw(num_balls_drawn)
        cnt = 0
        for j in range(len(expected_balls)):
            if expected_balls[j] in draw:
                draw.remove(expected_balls[j])
                cnt +=1
            else:
                break
            if cnt == len(expected_balls):
                M += 1
        

                
        hat_changing = copy.deepcopy(hat)
        
    return M/num_experiments           

hat = Hat(black=6, red=4, green=3)
probability = experiment(hat=hat,
                  expected_balls={'red':2,'green':1},
                  num_balls_drawn=5,
                  num_experiments=2000)

print(probability)