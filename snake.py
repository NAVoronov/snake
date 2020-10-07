from tkinter import *
import random
from tkinter import messagebox

#-------------------класс в котором всё окошко живёт--------------------
class field(Frame):

    #------------------------собственно конструктор класса-------------------------------------------------
    def __init__(self, master, fr_c = 'grey', s=20):
        self.fr_color = fr_c
        self.size=s
        self.snake=[]
        self.kol_x, self.kol_y=0,0

        super().__init__(master)
        self.pack(fill='both', expand='yes')        

        # типы движений
        self.mt={'Left'  : {'start' : 200, 'move' : (-1, 0), 'arr' : "first"},
            'Right' : {'start' : 20 , 'move' : (1, 0 ), 'arr' : "first"},
            'Up'    : {'start' : 110, 'move' : (0, -1), 'arr' : "first"},
            'Down'  : {'start' : 290, 'move' : (0, 1 ), 'arr' : "first"}
            }

        self.aft = None        
        self.key = "Right"

        self.score=0
        self.scorevar = StringVar()
        self.scorevar.set( str(self.score) )

        self.freq = 100
        self.freqvar = StringVar()
        self.freqvar.set( str(self.freq) )

        self.move = 0
        self.movevar = StringVar()
        self.movevar.set( str(self.move) )
        
        self.ap_x, self.ap_y = 0,0

        self.create_widgets()        

    #-------------------------------------------------------------------------        
    def create_widgets(self):
        frup = Frame(self)

        label1 = Label(frup, text="Съедено яблок : ")
        label1.pack(side=LEFT)
        label2 = Label(frup, textvariable = self.scorevar )
        label2.pack(side=LEFT)
        frup.pack(fill='x', side=TOP)

        label3 = Label(frup, text="Скорость игры : ")
        label3.pack(side=LEFT)
        label4 = Label(frup, textvariable = self.freqvar )
        label4.pack(side=LEFT)
        frup.pack(fill='x', side=TOP)

        label5 = Label(frup, text="Выполнено телодвижений : ")
        label5.pack(side=LEFT)
        label6 = Label(frup, textvariable = self.movevar )
        label6.pack(side=LEFT)
        frup.pack(fill='x', side=TOP)                

        fr = Frame(self, bg=self.fr_color)
        fr.pack(fill='both', side=TOP, expand='yes')

        self.c = Canvas(fr, bg=self.fr_color)
        self.c.pack(fill='both', expand='yes')
        self.c.focus_set()

        frb = Frame(self)
        info = Label(frb)
        info["text"] = "F5 - обновить игру. управление - стрелки. F9 - автомат. Alt+F4 - выход"
        info.pack(side=LEFT)
        frb.pack(fill='x', side=BOTTOM)

        self.c.bind("<KeyPress>", self.kp)   # клава
        self.c.bind("<Configure>", self.res) # изменение размеров окна
        self.c.bind("<MouseWheel>", self.mw) # колесо

    #------------------------изменения в размерах основного фрейма------------------------
    def res(self, e):
        self.width = e.width
        self.height = e.height
        self.refresh()
    #-------------------------------------------------------------------------

    #--------------------Колесико крутим - меняем масштаб-----------------------------------------------------    
    def mw(self, e):
        if e.delta < 0 and self.size > 10 : self.size-=1
        if e.delta > 0 and self.size < 50 : self.size+=1
        self.refresh()
    #-------------------------------------------------------------------------

    #-----------смотрим что нажато--------------------------------------------
    def kp(self, e):
        if e.keysym == "F5" : self.refresh()

        if e.keysym == "F9" : self.automove()
        
        #нажатия ток нужные берём
        if e.keysym not in ["Up","Down","Left","Right"] : return

        self.key=e.keysym

        self.move+=1
        self.movevar.set( str(self.move) )

        if self.aft == None : self.aft = self.after_idle( self.make_step )

    #-------------------------------------------------------------------------
    def make_step(self):
        self.aft = self.after(self.freq, self.make_step)

        self.one_step()
    #-------------------------------------------------------------------------
    def one_step(self):
        x = self.snake[-1]["x"] + self.mt[self.key]["move"][0]
        y = self.snake[-1]["y"] + self.mt[self.key]["move"][1]
        #в стенку упёрлись - по идее это смерть
        if x not in range(self.kol_x) or y not in range(self.kol_y):
            self.death()
            return

        # проверка на самоедство
        for i in self.snake:
            if [x,y] == [i["x"],i["y"]]:
                self.death()
                return                

        self.c.delete("arr")
        # была голова, а стало туловище
        self.snake[-1]["t"] = 0 

        #голова добавилась
        self.snake.append({'x': x, 'y': y, 't':1})

        # если съели яблоко - хвостик не трогаем
        if [self.ap_x, self.ap_y] == [self.snake[-1]["x"], self.snake[-1]["y"]]:
            self.score += 1
            self.scorevar.set( str(self.score) )
            self.freq -= 1
            self.freqvar.set( str(self.freq) )
            self.c.delete("apple")
            self.apple_gen()
        else: # иначе - хвостик убавился
            tstr = str(self.snake[0]["x"])+"-"+str(self.snake[0]["y"])
            self.c.delete(tstr)
            self.snake = self.snake[1:]

        # голова нарисовалась        
        self.c.create_oval(self.delta_x + self.snake[-1]["x"]*self.size,             self.delta_y + self.snake[-1]["y"]*self.size,
                           self.delta_x + self.snake[-1]["x"]*self.size + self.size, self.delta_y + self.snake[-1]["y"]*self.size + self.size,
                           fill="yellow", tag=str(self.snake[-1]["x"])+"-"+str(self.snake[-1]["y"]) )
        #и стрелочка, чтоб понять куды идём
        x = self.delta_x + self.snake[-1]["x"]*self.size + self.size*.5*abs(self.mt[self.key]["move"][1])                                                            
        y = self.delta_y + self.snake[-1]["y"]*self.size + self.size*.5*abs(self.mt[self.key]["move"][0])
        if self.key == "Right" : x+=self.size
        if self.key == "Down"  : y+=self.size
        self.c.create_line(x, y, x - self.mt[self.key]["move"][0], y - self.mt[self.key]["move"][1], tag='arr', arrow=self.mt[self.key]['arr'], fill="red"  )
    #-------------------------------------------------------------------------

    #----------------------смерть Каа...---------------------------------------------------
    def death(self):
        if self.aft != None : self.after_cancel( self.aft )
        
        messagebox.showinfo("Игра окончена", "Съели "+self.scorevar.get()+" яблок за "+self.movevar.get()+" движений.\n достигнута скорость игры в "+self.freqvar.get()+" единиц !")
        
        self.refresh()
    #-------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------
    def refresh(self):
        if self.aft != None : self.after_cancel( self.aft )
        self.aft = None        
##        self.key = ""        
        self.score = 0
        self.freq = 100
        self.move = 0
        self.scorevar.set( str(self.score) )
        self.freqvar.set ( str(self.freq) )
        self.movevar.set ( str(self.move) )

        self.CountSize()
            
        self.draw_field()

        self.snake.clear()
        self.snake.append({'x':self.kol_x//2-2, 'y':self.kol_y//2, 't':-1})
        self.snake.append({'x':self.kol_x//2-1, 'y':self.kol_y//2, 't':0})
        self.snake.append({'x':self.kol_x//2, 'y':self.kol_y//2, 't':1})
        self.draw_snake()

        self.apple_gen()
    #-------------------------------------------------------------------------
    def CountSize(self):
        self.kol_x, self.delta_x = divmod(self.width, (self.size))
        self.kol_y, self.delta_y = divmod(self.height,(self.size))

        self.delta_x //= 2
        self.delta_y //= 2
    #-------------------------------------------------------------------------
    #-------------------------------------------------------------------------
    def apple_gen(self):        
        rotten_apple=True
        while rotten_apple:
            self.ap_x, self.ap_y = random.randint(1,self.kol_x-2), random.randint(1,self.kol_y-2)
            rotten_apple=False
            for i in self.snake:
                if [self.ap_x, self.ap_y] == [i["x"], i["y"]] :
                    rotten_apple=True
                    break

        self.c.create_oval(self.delta_x + self.ap_x*self.size,             self.delta_y + self.ap_y*self.size,
                           self.delta_x + self.ap_x*self.size + self.size, self.delta_y + self.ap_y*self.size + self.size, fill="red", tag="apple" )
        return
    #-------------------------------------------------------------------------

    #------------------прорисовка поля-------------------------------------------------------        
    def draw_field(self):
        self.c.delete("all")        
        self.c.create_rectangle(self.delta_x, self.delta_y, self.delta_x+self.kol_x*self.size, self.delta_y+self.kol_y*self.size, tag="border")
    #-------------------------------------------------------------------------               

    #------------------прорисовка змейки-------------------------------------------------------        
    def draw_snake(self):
        for i in self.snake:
            self.c.create_oval(self.delta_x + i["x"]*self.size,             self.delta_y + i["y"]*self.size,
                               self.delta_x + i["x"]*self.size + self.size, self.delta_y + i["y"]*self.size + self.size, fill="yellow",
                               tag=str(i["x"])+"-"+str(i["y"]) )
        #и стрелочка, чтоб понять куды идём
        x = self.delta_x + self.snake[-1]["x"]*self.size + self.size*.5*abs(self.mt["Right"]["move"][1])                                                            
        y = self.delta_y + self.snake[-1]["y"]*self.size + self.size*.5*abs(self.mt["Right"]["move"][0])
        x+=self.size
        self.c.create_line(x, y, x - self.mt["Right"]["move"][0], y - self.mt["Right"]["move"][1], tag='arr', arrow="first", fill="red"  )            
    #-------------------------------------------------------------------------

    #-------------------автомат попробуем сделать------------------------------------------------------        
    def automove(self):
        self.aft = self.after(self.freq, self.automove)
        
        seek={"Right":0, "Left":0, "Down":0, "Up":0}
        seek[self.key] = 1 #приоритет движения - то направление куда шли до этого

        #надо понять где яблоко и стремиться к нему.
        if self.ap_x-self.snake[-1]["x"] > 0 : seek["Right"] += 2 #яблоко справа - идём вправо
        if self.ap_x-self.snake[-1]["x"] < 0 : seek["Left"] += 2 #иначе влево
        if self.ap_y-self.snake[-1]["y"] > 0 : seek["Down"] += 2 #яблоко ниже - идём вниз
        if self.ap_y-self.snake[-1]["y"] < 0 : seek["Up"] += 2 #иначе вверх

        #также исключим самоедство из списка телодвижений
        for j in seek:
            x = self.snake[-1]["x"] + self.mt[j]["move"][0]
            y = self.snake[-1]["y"] + self.mt[j]["move"][1]
            for i in self.snake:
                if [x,y] == [i["x"],i["y"]]:
                    seek[j] = -1000

        #если справа от головы граница - вправо не ходить !
        if self.snake[-1]["x"]+1 == self.kol_x : seek.pop("Right", 1)
        #если слева от головы граница - влево не ходить !
        if self.snake[-1]["x"]-1 == -1 : seek.pop("Left", 1)
        #если внизу от головы граница - вниз не ходить !
        if self.snake[-1]["y"]+1 == self.kol_y : seek.pop("Down", 1)
        #если вверху от головы граница - вверх не ходить !
        if self.snake[-1]["y"]-1 == -1 : seek.pop("Up", 1)

        max=-10000
        key=self.key
        for i in seek:
            if seek[i]>max:
                key = i
                max=seek[i]

        if key != self.key:
            self.move+=1
            self.movevar.set( str(self.move) )
            self.key=key
        
        self.one_step()

    #-------------------------------------------------------------------------

#-----------------------------------------------------------------------    

if (__name__ == "__main__"):
    random.seed() #запуск рандомайзера

    window=Tk()
    window.title("Змейка")
    window.wm_state('zoomed')
    window.minsize(width=800, height=600)
    
    app = field(window, "green", 20)    

    window.mainloop()
