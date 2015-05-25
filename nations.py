import random, time
LISTLOCATION = 'nation_list'

def load_list(listlocation = LISTLOCATION):
    with open(listlocation, 'r') as file:
        return [n for n in file.read().split('\n') if n]

def quiz(nationlist, asker, tries=3, practice=True):
    score = 0
    starttime = time.time()
    for nation in nationlist:
        othernations = nationlist[:]
        othernations.remove(nation)
        choices = random.sample(othernations, 3)
        choices.append(nation)
        random.shuffle(choices)
        for i in range(tries):
            answer = asker.ask(nation, choices)
            if answer == nation:
                score += tries - i
                break
            else:
                feedback = ['Incorrect',]
                if practice:
                    feedback.append(nation)
                asker.feedback(feedback)

    timetaken = time.time() - starttime

    asker.feedback((('Final score', score),
                    ('Out of', len(nationlist)*tries),
                    ('Time', timetaken),
                    ('Points per second', score/timetaken)))

class ConsoleAsker:
    def ask(self, prompt, options):
        print '-'*8
        for i, option in enumerate(options):
            print '%d) %s' %(i, option)

        error_message = 'Pleas enter a number between 0 and %d.' %(len(options)-1)
        while True:
            response = raw_input('? ')
            if not response.isdigit():
                print error_message
                continue
            n = int(response)
            if n < 0 or n >= len(options):
                print error_message
                continue
            return options[n]

    def feedback(self, feedback):
        for item in feedback:
            if isinstance(item, tuple) and len(item) == 2:
                key, value = item
                key, value = str(key), str(value)
                print '%s: %s' %(key, value)
            else:
                print str(item)

def demo():
    nationlist = load_list()
    asker = ConsoleAsker()
    quiz(nationlist, asker)
    raw_input('Press enter to quit')

if __name__ == '__main__':
    demo()
