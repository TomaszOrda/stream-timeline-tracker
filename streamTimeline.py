from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.reactive import reactive
from textual import events
from time import monotonic, strftime
import random, string, sys

class TimeDisplay(Static):
    """Built using textual tutorial"""
    start_time = reactive(monotonic)
    time = reactive(0.0)
    value = ""
    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1, self.update_time)
    def update_time(self) -> None:
        self.time =  (monotonic() - self.start_time)
    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.value =f"{hours:02,.0f}:{minutes:02.0f}:{seconds:02.0f}"
        self.update(self.value)
    def reset(self):
        self.start_time = monotonic()

class TimelineApp(App):
    CSS = """
    Input {
        border: none;
        height:auto;
    }
    """
    records = {}
    offset = 0
    stamp_title = None
    timestamp = None
    
    def compose(self) -> ComposeResult:
        self.identifier = f"{strftime('%Y-%m-%d')}{''.join(random.choices(string.ascii_letters, k=6))}"
        yield Static("Stream timeline tracker\n")
        self.time_field = TimeDisplay()
        yield self.time_field
        self.input_field = Input("")
        yield self.input_field
        self.title_field = Static("Title: ")
        yield self.title_field
        self.timestamp_field = Static("Timestamp: ")
        yield self.timestamp_field
        yield Static("Write help to print the guide.")
        self.help_field = Static("""
        help: close/open the guide\n
        title: set the title of a timestamp\n
        offset: add time to the timer; on default adds miliseconds;\n
             allowes for ±hh:±mm:±ss\n
             +/- are optional\n
        stamp/timestamp/time: set timestamp;\n
             default is current time;\n
             standard formating hh:mm:ss, however it can be set to any string\n
        restart/reset: restart the timer to 00:00:00\n
        enter empty field to perform default action: timestamp>title>next\n
        escape to exit the programm
        """)
        self.help_field.visible = False
        yield self.help_field
        with open(self.identifier+'.json', 'w') as file:    file.write("{\n")
        with open(self.identifier+'.txt',  'w') as file:    file.write("Timeline\n")

    def on_key(self, event: events.Key):
        if event.key == "enter":
            self.parseInput()
        elif event.key == "escape":
            if self.stamp_title and self.timestamp:
                doAction('next',None)
            with open(self.identifier+'.json', 'a') as file:    file.write("}")
            sys.exit()
    
    def parseInput(self):
        input_string = self.input_field.value.lstrip().split(' ',1)
        self.input_field.value = ""
        
        key = input_string[0]
        if len(input_string)>1:
            value = input_string[1]
        else:
            value = None
        self.doAction(key, value)
        
    def doAction(self, key, value):
        def isNumber(string):
            try:
                float(string)
                return True
            except ValueError:
                return False
                
        if key == 'title':
            self.stamp_title = str(value)
            self.title_field.update(f"Title: {self.stamp_title}")
        elif key == 'offset' and value:
            if isNumber(value):
                self.time_field.start_time -= float(value)/1000
            elif value[-2:]=="ms" and isNumber(value[:-2]):
                self.time_field.start_time -= float(value[:-2])/1000
            else:
                values = value.split(':')
                if all(list(map(isNumber, values))):
                    seconds = 0
                    unit = 1
                    for v in reversed(values):
                        seconds += float(v)*unit
                        unit = unit*60
                    self.time_field.start_time -= seconds
        elif key == 'stamp' or key == 'timestamp' or key == 'time':
            if value:
                self.timestamp = value
            else:
                self.timestamp = self.time_field.value
            self.timestamp_field.update(f"Timestamp: {self.timestamp}")
        elif key == 'restart' or key == 'reset':
            self.time_field.reset()
        elif key == "next":
            if not self.stamp_title:
                self.doAction('title', None)
            if not self.timestamp:
                self.doAction('timestamp', None)
                
            self.records[self.timestamp] = self.stamp_title
            with open(self.identifier+'.json', 'a') as file:    file.write(f"'{self.timestamp}':{self.stamp_title}\n")
            with open(self.identifier+'.txt' , 'a') as file:    file.write(f"{self.timestamp} {self.stamp_title}\n")
                
            self.stamp_title = None
            self.timestamp = None
            self.title_field.update("Title:")
            self.timestamp_field.update("Timestamp:")
        elif key == "help":
            self.help_field.visible = not self.help_field.visible
        elif key == "":
            if not self.timestamp:
                self.doAction("timestamp",None)
            elif not self.stamp_title:
                self.doAction("title",None)    
            else:
                self.doAction("next",None)    
        elif self.stamp_title == "":
            if(value):
                self.doAction("title",key + " " + str(value))
            else:
                self.doAction("title",key)
        
if __name__ == "__main__":
    TimelineApp().run()