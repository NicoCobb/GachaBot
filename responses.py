from random import choice

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'u quiet af'
    elif 'hell' in lowered:
        return 'heyyyy'
    elif 'asstarion' in lowered:
        return 'asstarion'
    else:
        return choice(['tf does that mean?',
                       'please say something clearer',
                       'try again thx <3'])
    
def bully_target_response() -> str:
    return choice (['Angela nobody asked',
                    'yap yap yap yap blah blah blahhhhhh',
                    'how about you meow for me instead?',
                    'silence woman',
                    'no u',
                    'this kitty doesn\'t know how to shut UP'])

#TODO: be nice to her sometimes
#random chance to respond