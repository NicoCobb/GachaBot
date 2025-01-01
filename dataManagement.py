import json
from datetime import datetime

#returns the new total of a given star rating after update
def save_new_image(star: int) -> int:
    starStr = str(star)
    empty= False
    with open('data.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            empty = True
    
    with open('data.json', 'w', encoding='utf-8') as f:
        if not empty:
            print(star)
            if 'starCounts' in data:
                print('star counts exists')
                if starStr in data['starCounts']:
                    print('star key exists in starCounts')
                    data['starCounts'][starStr] += 1
                else:
                    data['starCounts'][starStr] = 1
        else:
            data = {}
            data['starCounts'] = {}
            data['starCounts'][starStr] = 1
        
        json.dump(data, f, ensure_ascii=False, indent=4)
        return data['starCounts'][starStr]

def save_user_gems(user: str, gems: int) -> int:
    empty = False
    with open('data.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            empty = True

    with open('data.json', 'w', encoding='utf-8') as f:
        if not empty:
            if user in data:
                if 'gems' in data[user]:
                    data[user]['gems'] += gems
                else:
                    data[user]['gems'] = gems
            else:
                data[user] = {}
                data[user]['gems'] = gems

        else:
            data = {}
            data[user] = {}
            data[user]['gems'] = gems
        
        json.dump(data, f, ensure_ascii=False, indent=4)
        return data[user]['gems']

def load_gems(user: str) -> int:
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

def attempt_create_json() -> None:
    #create data.json if it doesn't exist yet
    try:
        open('data.json', 'x')
    except Exception as e:
        print(e)
