import random

IMAGENES = ['''

        +-----------+
        |           |
                    |
                    |
                    |
                    |
                    |
                    ==========''','''
        
        +-----------+
        |           |
        0           |
                    |
                    |
                    |
                    |
                    ==========''','''
        
        +-----------+
        |           |
        0           |
        |           |
                    |
                    |
                    |
                    ==========''','''


        +-----------+
        |           |
        0           |
       /            |
                    |
                    |
                    ==========''','''

        +-----------+
        |           |
        0           |
       / \          |
                    |
                    |
                    ==========''','''

        +-----------+
        |           |
        0           |
       /|\          |
        |           |
                    |
                    ==========''','''

        +-----------+
        |           |
        0           |
       /|\          |
        |           |
       /            |
                    ==========''','''

        +-----------+
        |           |
        0           |
       /|\          |
        |           |
       / \          |
                    ==========''']

PALABRAS = [
    
    'lavadora',
    'secadora',
    'silla',
    'mesa',
    'computador',
    'democracia',
    'politica',
    'puerta',
    'perro',
    'gato'
]

def random_word():
    
    idx = random.randint(0, len(PALABRAS) -1)
    return PALABRAS[idx]

def display(hidden_word, tries):
    print(IMAGENES[tries])
    print('')
    print(hidden_word)
    #print('__-__-__-__-__-__-')

def run():
    
    word = random_word()
    hidden_word = ['-'] * len(word)
    tries = 0
    
    letter_writes = [] # cod nuevo
         
    while True:
        
        display(hidden_word, tries)
        current_letter = str(input('escoje una letra: '))
        
        letter_writes.append(current_letter)
        print("Letras usadas ===> ", letter_writes)

        if current_letter.isdigit() == True:
            
            print("Letra incorrecta, digitaste un numero")
        
        else:
            
            letter_indexes = []
            
            for idx in range(len(word)):
                 
                if word [idx] == current_letter:
                    
                    letter_indexes.append(idx)
        
            if len(letter_indexes) == 0:
                tries += 1
                
                if tries == 7:
                    display(hidden_word, tries)
                    print('')
                    print('Perdiste !, la palabra correcta era {}'.format(word))
                    break
            else:
                for idx in letter_indexes:
                    hidden_word[idx] = current_letter
                
            try:
                hidden_word.index('-')
                
            except ValueError:
                
                print('')
                print('Ganaste ! La palabra es: {}'.format(word.upper()))
                print('Lo hiciste en {} intentos'.format(tries))
                break
            
if __name__=='__main__':
    
    print('BIENVENIDOS A AHORCADOS')
    run()