from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import facebook
import json
from fbtoken import *

def convert_unicode_to_string(x):
    return x.encode('ascii', 'ignore')

def fetch(topic):
    g = facebook.GraphAPI(ACCESS_TOKEN)
    posts = g.request("search", {'q' : topic, 'type' : 'post', 'limit': 20})
    postList = [post for post in posts['data']]
    message = []
    for post in postList:
        try:
            message.append(convert_unicode_to_string(post['message']))
        except:
            pass
    return message

def on_enter(instance):
    print type(instance.text)

class FacebookMining(App):
        
    def build(self):
        
        topic = 'Python'
        
        layout = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=(10,10,10,10))
        layout.bind(minimum_height=layout.setter('height'))
        message = fetch(topic)
        for data in message:
            l = Button(text=data, text_size=(300, None), size_hint_y=None, padding=(5, 5), bold=True)
            # calculating height here 
            before = l._label.render()
            l.text_size=(300, None)
            after = l._label.render()
            l.height = 60 + (after[1]/before[1])*before[1] # ammount of rows * single row height
            # end
            layout.add_widget(l)
            
        sub = ScrollView()
        sub.add_widget(layout)
        
        root = GridLayout(cols=1)
        
        title = Label(text='Facebook Mining Topic: ' + topic, font_size=30, size_hint_y=None, height=100)
        root.add_widget(title)
        
        textinput = TextInput(hint_text='Search ...', multiline=False, size_hint_y=None, height=40)
        textinput.bind(on_text_validate=on_enter)
        root.add_widget(textinput)
        
        root.add_widget(sub)
        return root
        

if __name__ == '__main__':
    FacebookMining().run()
