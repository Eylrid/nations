import random, time, os, pickle
LISTLOCATION = 'nation_list'
TRACKERLOCATION = 'nationtracker.pkl'

def load_list(listlocation = LISTLOCATION):
    with open(listlocation, 'r') as file:
        return [n for n in file.read().split('\n') if n]

def load_tracker(trackerlocation=TRACKERLOCATION):
    if os.path.exists(trackerlocation):
        with open(trackerlocation, 'r') as file:
            nationtracker = pickle.load(file)
            nationtracker.start()
            return nationtracker
    else:
        nationlist = load_list()
        return NationTracker(nationlist)

def save_tracker(nationtracker, trackerlocation=TRACKERLOCATION):
    with open(trackerlocation, 'w') as file:
        pickle.dump(nationtracker, file)

class NationTracker:
    LATESTVERSION = 3
    def __init__(self, nationlist):
        self.nationlist = nationlist[:]
        self.create_pairscores()
        self.version = NationTracker.LATESTVERSION
        self.start()

    def create_dictionary(self):
        self.pairscores = {}
        for nation1 in self.nationlist:
            self.pairscores[nation1] = {}
            for nation2 in self.nationlist:
                if nation1 == nation2: continue
                self.pairscores[nation1][nation2] = [1,1]

    def start(self):
        self.index = 0
        self.check_version()

    def check_version(self):
        if not hasattr(self, 'version'):
            self.version = 1

        if self.version == 1:
            self.pairscores = self.dictionary
            del self.dictionary
            self.version = 2

        if self.version == 2:
            self.nationscores = {}
            for nation in self.nationlist:
                right = 1
                wrong = 1
                for r, w in self.pairscores[nation].values():
                    right += r-1
                    wrong += w-1
                self.nationscores[nation] = [right, wrong]

            self.version = 3

    def next(self):
        if self.index == len(self.nationlist):
            raise StopIteration

        nation = self.nationlist[self.index]

        othernations = self.nationlist[:]
        othernations.remove(nation)
        random.shuffle(othernations)

        def sort_key(nation2):
            right = self.pairscores[nation][nation2][0]
            wrong = self.pairscores[nation][nation2][1]
            return float(right)/float(wrong)

        othernations.sort(key=sort_key)
        choices = othernations[:3]
        choices.append(nation)
        random.shuffle(choices)
        self.index += 1
        return nation, choices

    def mark(self, correct, answer, options):
        if answer != correct:
            #incorrect answer, mark wrong
            self.pairscores[correct][answer][1] += 1
            self.nationscores[correct][1] += 1
        else:
            self.nationscores[correct][0] += 1

        for option in options:
            if option != correct and option != answer:
                #incorrect option that wasn't choosen, mark right
                self.pairscores[correct][option][0] += 1

    def score(self, nation):
        right, wrong = self.nationscores[nation]
        return float(right)/float(wrong)

class Quizer:
    def __init__(self, nationtracker, tries=3, practice=True):
        self.nationtracker = nationtracker
        self.tries = tries
        self.practice = practice
        self.score = 0

    def start(self):
        self.starttime = time.time()

    def next(self):
        self.attempts = 0
        self.correctanswer, self.choices = self.nationtracker.next()
        return self.correctanswer, self.choices

    def answer(self, answer):
        self.nationtracker.mark(self.correctanswer, answer, self.choices)
        if answer == self.correctanswer:
            self.score += self.tries - self.attempts
            return 'correct'
        else:
            self.attempts += 1
            if self.attempts >= self.tries:
                return 'move_on'
            return 'try_again'

    def end(self):
        save_tracker(self.nationtracker)
        possible_score = len(self.nationtracker.nationlist)*self.tries
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
    nationtracker = load_tracker()
    asker = ConsoleAsker(nationtracker)
    asker.quiz()
    save_tracker(nationtracker)
    raw_input('Press enter to quit')

if __name__ == '__main__':
    demo()
