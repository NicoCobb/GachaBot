import json

#user: gem
#TODO: tie gems to specifics users
def save(g: int) -> None:
    #write and save
    data = {
        'gemCount': g
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_gems() -> int:
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
            return
        
    if not 'gemCount' in data:
        return 0
    else:
        return data['gemCount']