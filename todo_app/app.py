from flask import request,redirect,url_for,Response,Flask,render_template
from todo_app.flask_config import Config
from todo_app.data import session_items
import requests
import os
import json

app = Flask(__name__)
app.config.from_object(Config)

def get_trello_API_credentials():
    f = open("todo_app/Trello_API_Keys.txt", "r").read().split("\n")
    return {'key': f[0], 'token': f[1]}

payload = get_trello_API_credentials()

class Trello_Data:
    def __init__(self):
        self.boards_names_and_ref = {}
        self.lists_names_and_ref = {}
        self.cards_names_and_ref = {}
        self.todo_list_with_cards = {}
        self.doing_list_with_cards = {}
        self.done_list_with_cards = {}

    def get_trello_boards_name_and_ref(self):
        list_level = 0
        boards_data_response = requests.get('https://api.trello.com/1/members/me/boards?', params=payload)
        boards_data = json.loads(boards_data_response.content)
        for i, board in enumerate(boards_data):
            list_level = i
            self.boards_names_and_ref[boards_data[list_level]['name']] = boards_data[list_level]['id']
            list_level += 1
    
    # def get_trello_cards_on_board(self, board_name):
    #     ref = self.boards_names_and_ref[board_name]
    #     cards_data_response = requests.get('https://api.trello.com/1/boards/' + ref + '/cards?', params=payload)
    #     cards_data = json.loads(cards_data_response.content)
    #     for i, list_name in enumerate(cards_data):
    #         list_level = i
    #         self.cards_names_and_ref[cards_data[list_level]['name']] = {'id':[cards_data[list_level]['id']], 'idLIst': [cards_data[list_level]['idList']]}
    #         list_level += 1
    
    def get_trello_lists_on_board(self, board_name):
        ref = self.boards_names_and_ref[board_name]
        lists_data_response = requests.get('https://api.trello.com/1/boards/' + ref + '/lists?', params=payload)
        list_data = json.loads(lists_data_response.content)
        for i, list_name in enumerate(list_data):
            list_level = i
            self.lists_names_and_ref[list_data[list_level]['name']] = list_data[list_level]['id']
            list_level += 1
    
    def get_trello_cards_on_list(self, list_name):
        ref = self.lists_names_and_ref[list_name]
        cards_on_list_data_response = requests.get('https://api.trello.com/1/lists/' + ref + '/cards?', params=payload)
        card_data = json.loads(cards_on_list_data_response.content)
        # self.list_with_cards['name']=self.lists_names_and_ref[list_name]
        # self.list_with_cards['id']=list_data[0]['id']
        for i, card_name in enumerate(card_data):
            list_level = i
            if card_data[list_level]['idList'] == self.lists_names_and_ref['Things To Do']:
                self.todo_list_with_cards[card_data[list_level]['name']] = card_data[list_level]['id']
                list_level += 1
            elif card_data[list_level]['idList'] == self.lists_names_and_ref['Doing']:
                self.doing_list_with_cards[card_data[list_level]['name']] = card_data[list_level]['id']
                list_level += 1
            elif card_data[list_level]['idList'] == self.lists_names_and_ref['Done']:
                self.done_list_with_cards[card_data[list_level]['name']] = card_data[list_level]['id']
                list_level += 1

class myTrello(Trello_Data):
    def get_my_board_info(self):
        return self.boards_names_and_ref
    def get_my_list_info(self, board_name):
        return self.lists_names_and_ref
    def get_cards_on_todo_list(self, list_name):
        return self.todo_list_with_cards
    def get_cards_on_doing_list(self, list_name):
        return self.doing_list_with_cards
    def get_cards_on_done_list(self, list_name):
        return self.done_list_with_cards

@app.route('/', methods=['GET'])
def index():
    myboards = myTrello()
    myboards.get_trello_boards_name_and_ref()
    boards = list(myboards.get_my_board_info().keys())
    return render_template('Index.html', boards=boards)

@app.route('/board/<board_name>', methods=['POST', 'GET', 'PUT'])
def go_to_board_tasks(board_name):
    myboards = myTrello()
    myboards.get_trello_boards_name_and_ref()
#    myboards.get_trello_cards_on_board(board_name)
    myboards.get_trello_lists_on_board(board_name)
    #cards = myboards.get_my_card_info(board_name)
    lists = myboards.get_my_list_info(board_name)
    list_keys = list(lists.keys())
    todo_list = list_keys[0]
    doing_list = list_keys[1]
    done_list = list_keys[2]
    myboards.get_trello_cards_on_list(todo_list)
    myboards.get_trello_cards_on_list(doing_list)
    myboards.get_trello_cards_on_list(done_list)
    todo_cards = myboards.get_cards_on_todo_list(todo_list)
    doing_cards = myboards.get_cards_on_doing_list(doing_list)
    done_cards = myboards.get_cards_on_done_list(done_list)
    if request.method == 'POST':
       payload_data = payload.copy()
       payload_data['idList'] = request.form['idList']
       payload_data['name'] = request.form['title']
       requests.post('https://api.trello.com/1/cards', params=payload_data)
       return redirect(url_for('index'))
    else:   
        return render_template('boardtasks.html', lists=lists, todo_cards=todo_cards, doing_cards=doing_cards, done_cards=done_cards)

@app.route('/lists/<board_name>')
def go_to_board_lists(board_name):
    myboards = myTrello()
    myboards.get_trello_boards_name_and_ref()
    myboards.get_trello_lists_on_board(board_name)
    lists = myboards.get_my_list_info(board_name)
    return render_template('my_lists.html', lists=lists)


# myboards = myTrello()
# myboards.get_trello_boards_name_and_ref()
# myboards.get_trello_cards_on_board('DevOps Module 2')
# myboards.get_trello_lists_on_board('DevOps Module 2')
# myboards.get_trello_cards_on_list('Doing')



# print(myboards.list_with_cards)