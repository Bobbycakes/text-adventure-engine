import string #Unused. using stuff like string.lower() doesn't seem to work? I'm just leaving this here anyways.
import random

rooms = {
	'entrance': {
		'items': ['sword', 'book'],
		'west': 'bathroom',
	},
	'bathroom': {
		'items': ['soap'],
		'east': 'entrance',
		'west': 'hiding space'
	},
	'hiding space': {
		'items': ['spoon', 'nuke',],
		'east': 'bathroom',
	},
	'elevator (floor 3)': {
		'items': [],
		'south': 'entrance',
		'down': 'elevator (floor 2)',
	},
	'elevator (floor 2)': {
		'items': [],
		'south': 'Room of Death',
		'up': 'elevator (floor 3)',
	},
	'Room of Death': {
		'items': ['sword', 'couch', 'beercase'],
		'north': 'elevator (floor 2)',
		'npc': ['spider'],
	},
}

current_room = 'entrance' #Default start room.
all_directions = ['north', 'south', 'east', 'west', 'up', 'down'] #This never changes. Defines all possible directions.
inv = ['Empty Slot' for _ in range(3)] #Make the inventory

#Define Important Things:
response = None #So we don't get yelled at later.
item_target = None
def cmd_help():
	print()
	print("HELP:")
	print()
	print("COMMANDS:")
	print("Use 'take' to take an item.")
	print("Use 'go' to go somewhere.")
	print("Use 'use' to use something.")
	print("Use 'eat' to eat a food item.")
	print("use 'drop' to drop an item. Note that when you drop an item it will stay in the room you dropped it in!")
	print("Use 'help' to open this dialog.")
	print()
	print("NOTES FOR IDIOTS:")
	print("You can only use items that are in your inventory.")
	print("You can only use the aforementioned on items that are in the room you are currently in.")
	print("If you want to use an inventory item on another inventory item, drop the targeted item beforehand.")
	print("If you want to use something on yourself, type 'self' when asked what to use the item on.")
def cmd_take(item_target):
	global current_room
	global rooms
	global inv
	items = rooms[current_room]['items']
	if item_target in rooms[current_room]['items'] and 'Empty Slot' in inv:
		print("You grab the %s." % item_target)
		empty_slot_index = inv.index('Empty Slot')
		inv[empty_slot_index] = item_target
		items.remove(item_target)
		print("Current inv:")
		print()
		print(inv)
	elif 'Empty Slot' not in inv:
		print("Error: Your inventory is full!")
	else:
		print("Error: I have no idea what you're talking about.")
		
def cmd_use(l_inv_use_target, l_use_target): #Check if input is valid.
	if l_inv_use_target not in inv:
		print("Error: You can't use %s, it's not in your inventory!" % l_inv_use_target)
	if l_use_target not in rooms[current_room]['items'] and l_use_target != 'self':
		print("Error: You can't use %s on something that's not in the room!" % l_inv_use_target)	
	if l_inv_use_target in inv and (l_use_target in rooms[current_room]['items'] or l_use_target == 'self'):
		print("debug dialog: input valid, passing to valid_cmd_use")
		valid_cmd_use(l_inv_use_target, l_use_target)
def cmd_eat():
	print("nom nom nom")
		
def valid_cmd_use(invuse, use): #Now that input is valid we can do a ton of conditionals.
	print("You use the %s on the %s." % (invuse, use))
	if invuse == 'sword':
		print("The sword breaks! Oh no...")
		loc = inv.index('sword') #We're finding the location of the sword so we can replace it with 'Empty Slot'
		inv.remove('sword')
		inv.insert(loc, 'Empty Slot')
		if use == 'soap':
			print()
			print("You cut the soap in half, revealing a key. You can now go north in the entrance.")
			rooms['entrance'].update({'north': 'elevator (floor 3)'})
			items = rooms[current_room]['items']
			loc = items.index('soap')
			items[loc] = ('soap residue')
			
	if invuse == 'nuke':
		loc = inv.index('nuke')
		inv.remove('nuke')
		inv.insert(loc, 'Empty Slot')
		print("""
                             ____
                     __,-~~/~    `---.
                   _/_,---(      ,    )
               __ /        <    /   )  \___
- ------===;;;'====------------------===;;;===----- -  -
                  \/  ~"~"~"~"~"~\~"~)~"/
                  (_ (   \  (     >    \)
                   \_( _ <         >_>'
                      ~ `-i' ::>|--"
                          I;|.|.|
                         <|i::|i|`.
                        (` ^'"`-' ")
-------------------------------------------------------------------------------
""")
def cmd_drop(droptarget):
	global rooms
	global current_room
	if droptarget not in inv:
		print("Error: You can't drop something you don't have.")
	else:
		loc = inv.index(droptarget)
		inv.remove(droptarget)
		inv.insert(loc, 'Empty Slot')
		print("You dropped the %s" % droptarget)
		rooms[current_room]['items'].append(droptarget)
def cmd_attack(target):
	for x in range(1,51):
		print(" ")
	global inv
	print("You entered attack mode.")
	if 'sword' not in inv:
		print("Get a sword!")
		print("You exited attack mode.")
		print(" ")
		prompt()
	if 'sword' in inv:
		hitpower = random.randint(50, 100)
		print("You attack the %s with your sword and an attack power of %s" % (target, hitpower))
		
def cmd_inv():
	print("Here's your current inventory.")
	print(inv)
def prompt():
  global current_room 
  global all_directions
  print()
  print("You are in the %s." % current_room)
  print("You can go %s " % (', '.join([d for d in all_directions if d in rooms[current_room]])))
  if 'npc' in rooms[current_room]:
  	print("There's a %s nearby." % (', '.join(rooms[current_room]['npc'])))
  if not rooms[current_room]['items']:
  	print("You don't see anything in the room with you.")
  else:
  	print("You see %s in the room with you." % (', '.join(rooms[current_room]['items'])))
  print()
  return input("What do you want to do?")
  
def go_to_room(target): #Check if the player is allowed to go in that direction. If that's true, set a target.
	global current_room
	current_room = target

def cmd_go(direction):
	if direction in rooms[current_room] and direction in all_directions:
		go_to_room(rooms[current_room][direction]) #The arguument for go_to_room is the target room.
	else:
		print("Error: You can't go %s from here." % direction)

#Sexy ASCII Welcome Screen

print()
print()
print("""

 _______  ______    __   __  _______         __    _  _______  ___   _  __   _______ 
|       ||    _ |  |  | |  ||  _    |       |  |  | ||   _   ||   | | ||  | |       |
|    ___||   | ||  |  | |  || |_|   | ____  |   |_| ||  |_|  ||   |_| ||__| |  _____|
|   | __ |   |_||_ |  |_|  ||       ||____| |       ||       ||      _|     | |_____ 
|   ||  ||    __  ||       ||  _   |        |  _    ||       ||     |_      |_____  |
|   |_| ||   |  | ||       || |_|   |       | | |   ||   _   ||    _  |      _____| |
|_______||___|  |_||_______||_______|       |_|  |__||__| |__||___| |_|     |_______|

  """)
print()
print("""
 _          _______   _________   _______   
( \        (  ___  )  \__   __/  (  ____ )  
| (        | (   ) |     ) (     | (    )|  
| |        | (___) |     | |     | (____)|  
| |        |  ___  |     | |     |     __)  
| |        | (   ) |     | |     | (\ (     
| (____/\  | )   ( |  ___) (___  | ) \ \__  
(_______/  |/     \|  \_______/  |/   \__/  
                                            
""")
print()
print("Welcome to Grub-Nak's Lair.")
print()
print("use command help or abbreviation h for a list of useful commands.")
print()

#Main Loop (> w <)

while True:
	response = prompt()
	if response == ("help") or response == ("h"):
		cmd_help()
		
	if response.startswith('eat '):
		cmd_eat()
	if response.startswith('go '):
		direction_target = response.split(" ")
		cmd_go(direction_target[1])
	if response.startswith('take '):
		item_target = response.split(" ")
		cmd_take(item_target[1])
	if response.startswith('use '):
		inv_use_target = response.split(" ")
		use_target = input("Use %s on what?" % inv_use_target[1])
		cmd_use(inv_use_target[1], use_target)
	if response.startswith('inv '): #Kind of deprecated, but continuity with previous conditionals is nice.
		cmd_inv()
	if response.startswith('drop '): #Command for dropping items and appending them back top the room items.
		inv_drop_target = response.split(" ")
		cmd_drop(inv_drop_target[1])
	if response == ("inv"):
		cmd_inv()
	if response.startswith('attack '):
		attack_target = response.split(" ")
		cmd_attack(attack_target[1])
