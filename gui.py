import nations
import Tkinter, tkMessageBox
import Image, ImageTk
import os

class Asker(Tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        Tkinter.Frame.__init__(self, master)
        self.quizer = nations.Quizer(*args, **kwargs)

        self.flagwidth = 400
        self.flagheight = 200
        self.margin = 50

        self.create_widgets()
        self.quizer.start()
        self.next()

    def create_widgets(self):
        self.prompt_label = Tkinter.Label(self, text='prompt')
        self.prompt_label.grid(row=0, column=0)

        canvaswidth = self.flagwidth*2 + self.margin*3
        canvasheight = self.flagheight*2 + self.margin*3
        self.canvas = Tkinter.Canvas(self, width=canvaswidth, height=canvasheight)
        self.canvas.grid(row=1, column=0)

        self.tkimages = []
        self.images = []
        i = 0
        for x in range(2):
            xcoord = self.margin + self.flagwidth/2 + (self.flagwidth+self.margin)*x
            for y in range(2):
                ycoord = self.margin + self.flagheight/2 + (self.flagheight+self.margin)*y
                im = Image.new('RGB', (self.flagwidth, self.flagheight), '#000000')
                tkimage = ImageTk.PhotoImage(im)
                self.tkimages.append(tkimage)
                canvasimage = self.canvas.create_image(xcoord, ycoord,
                                                       image=tkimage,
                                                       anchor='center',
                                                       tags=('flag', i))
                i += 1
                self.images.append(canvasimage)

        self.canvas.tag_bind('flag', '<Button-1>', self.click)

    def next(self):
        try:
            self.prompt, self.options = self.quizer.next()
        except StopIteration:
            self.end()
            return

        self.prompt_label['text'] = self.prompt

        for i in range(4):
            option = self.options[i]
            option = option.replace(' ', '_')+'.png'
            filename = os.path.join('flags', option)
            im = Image.open(filename)
            im.thumbnail((self.flagwidth, self.flagheight))
            tkimage = ImageTk.PhotoImage(im)
            self.tkimages[i] = tkimage
            self.canvas.itemconfig(self.images[i], image=tkimage)

    def click(self, event):
        tags = self.canvas.gettags('current')
        i = int(tags[1])
        answer = self.options[i]
        result = self.quizer.answer(answer)
        if result == 'try_again':
            tkMessageBox.showerror('Incorrect', 'Incorrect. Try Again.')
        elif result == 'move_on':
            tkMessageBox.showerror('Incorrect', 'Incorrect. Moving on.')
            self.next()
        else:
            self.next()

    def end(self):
        score, possible_score, timetaken, pointspersecond = self.quizer.end()
        message = '''
Score: %d
Out of: %d
Time: %f
Points per Second: %f
''' %(score, possible_score, timetaken, pointspersecond)
        tkMessageBox.showinfo('Results', message)
        self.quit()


def main():
    rt = Tkinter.Tk()
    nationlist = nations.load_list()[:80]
    asker = Asker(rt, nationlist)
    asker.grid()
    asker.mainloop()

if __name__ == '__main__':
    main()
