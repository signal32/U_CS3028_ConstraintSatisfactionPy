#import lm_Conditions as lmcs
from LetsMeet.ConditionManager import variable
from LetsMeet.ConditionManager.ConditionSet import ConditionSet
from sys import maxsize
from tkinter.ttk import Treeview
import LetsMeet as lm
from datetime import date, datetime

import tkinter as tk
import tkinter.ttk as ttk

from forms import *


class Application(tk.Frame):
    def __init__(self, root) -> None:
        self.root = root
        self.UI()
        self.events = []
        self.selection = {}

    # Initilaise UI
    def UI(self):
        #Configure application root
        self.root.title("Let's Meet Tech Demo")
        self.root.grid_rowconfigure(1, minsize=1)
        self.root.grid_columnconfigure(4, minsize=1)

        #Define UI widgets
        self.addEventButton = tk.Button(self.root,text="Add Event",command=self.addEvent)
        self.addEventButton.grid(row=0,column=0,sticky='nsew')

        self.setDatesButton = tk.Button(self.root,text="Add event date",command=lambda: EnterDateRange(self.root,self.setDateRange))
        self.setDatesButton.grid(row=1,column=0,sticky='nsew')

        self.setUsersButton = tk.Button(self.root,text="Add required user")
        self.setUsersButton.grid(row=1,column=1,sticky='nsew')

        self.idnumber_label = tk.Label(self.root, text="Name:")
        self.idnumber_entry = tk.Entry(self.root)
        self.idnumber_label.grid(row=0, column=1, sticky=tk.W)
        self.idnumber_entry.grid(row=0, column=2,sticky='nsew')

        self.spewButton = tk.Button(self.root, text="Debug Selected", command=self.debug)
        self.spewButton.grid(row=1,column=4)

        # Set treeview
        self.tree = ttk.Treeview(self.root,columns=('Value','Type','ID'))

        # Set headings
        self.tree.heading('#0',text='Item')
        self.tree.heading('#1',text='Value')
        self.tree.heading('#2',text='Type')
        self.tree.heading('#3',text='ID')

        # Set attribites
        self.tree.column('#0', width=150, minwidth=100, stretch=tk.YES)
        self.tree.column('#1', stretch=tk.YES)
        self.tree.column('#2', stretch=tk.YES)        
        self.tree.column('#3', stretch=tk.YES)

        #self.eventFolder = self.tree.insert("",0,text="Event",values=(str(eventManager.event.name),"Collection",str(eventManager.event.uuid)))        
        #self.userFolder = self.tree.insert("",1,text="Users",values=("","Collection"))

        self.tree.grid(row=4, columnspan=9, sticky='nsew')
        self.treeview = self.tree

        self.id = 0
        self.iid = 0

    def popupUser(self):
        self.popupUser

    def debug(self):
        print("______Selected_______")
        print("ID: ",self.getCurrentValues())
        print("Contents: ",self.getCurrentTreeID())
        print("Children: ", self.treeview.get_children(self.getCurrentTreeID()))
        print("_______Global________")
        print("Events: ", self.events)

    def getCurrentTreeID(self):
        try:
            return self.treeview.selection()[0]
        except:
            raise Exception("ERR: No selection found")

        
    def getCurrentValues(self):
        try:
            return self.treeview.item(self.treeview.focus())['values']
        except:
            raise Exception("ERR: No selection found")
 

    """returns the event object with specified UUID"""
    def getEvent(self,uuid)-> lm.EventManager.Event:
        for event in self.events:
            if str(event.uuid) == uuid:
                return event

        raise Exception("ERR: Event not found") 

    def insert_data(self):
        self.treeview.insert('', 'end', iid=self.iid, text="Item_" + str(self.id),
                            values=("Name: " + self.name_entry.get(),
                                    self.idnumber_entry.get()))
        self.iid = self.iid + 1
        self.id = self.id + 1

    def addEvent(self):
        event = lm.EventManager.Manager()
        event.initBlank()
        if(len(self.idnumber_entry.get())>1):
            event.setProperty('name',self.idnumber_entry.get())
        self.events.append(event.event)
        root = self.treeInsert(event.event)
        self.treeInsert("DOMAINHOLDER",root)
        self.treeInsert("CONSTRAINTHOLDER",root)
        self.treeInsert("USERHOLDER",root)

    def insertDomain(self,event:bool, name, value, id, ):
        if event:
            x = self.eventFolder
        else:
            x = 'User'
        self.treeview.insert(x,'end',iid=self.iid,text=str(name),values=(str(value),"Domain",str(id)))
        self.iid = self.iid + 1
        self.id = self.id + 1

    def treeInsert(self,element,parent = None):
        #current = self.treeview.item(self.treeview.focus())
        #item = self.treeview.selection()[0]
        insertID = self.iid
        if isinstance(element,lm.EventManager.Event):
            self.treeview.insert('','end',iid=self.iid,text=str(element.name),values=("","Event",str(element.uuid)))
        elif isinstance(element,variable.Variable):
            self.treeview.insert(parent,'end',iid=self.iid,text=str(element.name),values=(str(element.domain),"Variable",str(element.uuid)))
        elif element == "CONSTRAINTHOLDER":
            self.treeview.insert(parent,'end',iid=self.iid,text=str("Constraints"),values=("","ui_ConstraintGroup",str(self.iid)))
        elif element == "DOMAINHOLDER":
            self.treeview.insert(parent,'end',iid=self.iid,text=str("Domains"),values=("","ui_DomainGroup",str(self.iid)))
        elif element == "USERHOLDER":
            self.treeview.insert(parent,'end',iid=self.iid,text=str("Users"),values=("","ui_UserGroup",str(self.iid)))
        
        self.iid = self.iid + 1
        self.id = self.id + 1

        return insertID
    
    # Sets date range on selected event
    def setDateRange(self,d1_d,d1_m,d1_y,d2_d,d2_m,d2_y):
        man = lm.ConditionManager.Manager()
        man.event = self.getEvent(self.getCurrentValues()[2])
        val = man.setDateRange(datetime(d1_y,d1_m,d1_d),datetime(d2_y,d2_m,d1_d))
        self.treeInsert(val,self.treeview.get_children(self.getCurrentTreeID())[0])
           
    def addUserdateRange(self,d1_d,d1_m,d1_y,d2_d,d2_m,d2_y):
        event = self.getEvent(self.getCurrentValues()[2])
        cond = lm.ConditionManager.ConditionSet()
        #cond.addVariable(lm.ConditionManager)


if __name__ == "__main__":
    
    # Get ourselves a manager
    eventManager = lm.EventManager.Manager()
    eventManager.initBlank()

    # get an condition manager
    conditionManager = lm.ConditionManager.Manager()
    conditionManager.event = eventManager.event # This is a bodge to get around lack of pointers in python
    c1 = conditionManager.getID()
    
    print(conditionManager.conditionSet)

    

    app = Application(tk.Tk())
    app.root.mainloop()