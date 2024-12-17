import json
from datetime import datetime


def save_user_gems(user: str, gems: int) -> int:
    file_exists = True
    print('printoooooo')
    with open('data.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            file_exists = False


    with open('data.json', 'w', encoding='utf-8') as f:
        if file_exists:
            if user in data:
                print('got here')
                if 'gems' in data[user]:
                    print(f"got here and gems is {data[user]['gems']} and add is {gems}")
                    data[user]['gems'] += gems
                else:
                    print('hit the else')
                    data[user]['gems'] = gems
            else:
                print('final else')
                data[user] = {}
                data[user]['gems'] = gems

        else:
            data = {}
            data[user] = {}
            data[user]['gems'] = gems
        
        json.dump(data, f, ensure_ascii=False, indent=4)
        return data[user]['gems']

def load_gems(user: str) -> int:
    #create data.json if it doesn't exist yet
    try:
        f = open('data.json', 'x')
    except Exception as e:
        print(e)
    
    with open('data.json', 'r') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            print('empty file')
            return 0
        
    if data[user]['gems']:
        return data[user]['gems']
    else:
        return 0

    
    # def check_daily() -> None:
