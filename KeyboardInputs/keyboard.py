import keyboard
# while True:
#     try: 
#         if keyboard.is_pressed('q'): 
#             print('You Pressed A Key!')
#             break 
#         else:
#             pass
#     except:
#         break

while True:
    if keyboard.is_pressed('u'):
        print(0)
    elif keyboard.is_pressed('j'):
        #keyboard.press_and_release('s')
        print(1)
    elif keyboard.is_pressed('k'):
         #keyboard.press_and_release('d')
         print(2)
    elif keyboard.is_pressed('h'):
        #keyboard.press_and_release('a')
        print(3)
    else:
        print(4)
        keyboard.release('w')