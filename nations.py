import random, time
LISTLOCATION = 'nation_list'

def load_list(listlocation = LISTLOCATION):
    with open(listlocation, 'r') as file:
        return [n for n in file.read().split('\n') if n]

def question_generator(nationlist):
    for nation in nationlist:
        othernations = nationlist[:]
        othernations.remove(nation)
        choices = random.sample(othernations, 3)
        choices.append(nation)
        random.shuffle(choices)
        yield nation, choices

class Quizer:
    def __init__(self, nationlist, tries=3, practice=True):
        self.nationlist = nationlist
        self.tries = tries
        self.practice = practice
        self.score = 0
        self.questions = question_generator(nationlist)

    def start(self):
        self.starttime = time.time()

    def next(self):
        self.attempts = 0
        self.correctanswer, self.choices = self.questions.next()
        return self.correctanswer, self.choices

    def answer(self, answer):
        if answer == self.correctanswer:
            self.score += self.tries - self.attempts
            return 'correct'
        else:
            self.attempts += 1
            if self.attempts >= self.tries:
                return 'move_on'
            return 'try_again'

    def end(self):
        possible_score = len(self.nationlist)*self.tries
        timetaken = time.time() - self.starttime
        pointspersecond = self.score/timetaken
        return self.score, possible_score, timetaken, pointspersecond

class ConsoleAsker:
    def __init__(self, *args, **kwargs):
        self.quizer = Quizer(*args, **kwargs)

    def quiz(self):
        self.quizer.start()
        prompt, options = self.quizer.next()
        while True:
            print '-'*8
            for i, option in enumerate(options):
                print '%d) %s' %(i, option)

            error_message = 'Please enter a number between 0 and %d.' %(len(options)-1)
            while True:
                response = raw_input('? ')
                if not response.isdigit():
                    print error_message
                    continue
                n = int(response)
                if n < 0 or n >= len(options):
                    print error_message
                    continue
                answer = options[n]
                result = self.quizer.answer(answer)
                if result == 'try_again':
                    print 'Incorrect,', prompt
                else:
                    break

            try:
                prompt, options = self.quizer.next()
            except StopIteration:
                break

        score, possible_score, timetaken, pointspersecond = self.quizer.end()
        print 'Score: %d' %score
        print 'Out of: %d' %possible_score
        print 'Time: %f' %timetaken
        print 'Points per Second: %f' %pointspersecond


def demo():
    nationlist = load_list()
    asker = ConsoleAsker(nationlist)
    asker.quiz()
    raw_input('Press enter to quit')

if __name__ == '__main__':
    demo()
