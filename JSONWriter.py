"""
Program Name: JSON Writer
Purpose: To easily be able to add items, NPCs, enemies, and more to JSON files.
Author: Isaiah Wegwitz
Last Modified: 12/03/2025
"""
import json
import sys
import os.path

"""
Features I still need to implement:
1. I need to make it auto-assign ID values to the items. It should always count up, unless a number is missing (from an item being deleted), in which case, it fills in gaps.
2. I need to be able to add more than just weapons to the items.
3. I need to be able to add NPCs and Enemies as well.
4. The ID values should be different ranges depending on if they are an item, NPC, or Enemy, that way there is no overlap.
5. I might consider making it so the traits system is separate, in which case I just make base items, NPCs, and Enemies, and the RPG itself handles the traits. For example, 
    I'd make a sword, then the game would decide if the sword is metal, wood, or stone, if it's fragile, if it's magic, blessed, elemental, all that stuff.
"""

def readAllEntries(entries):
    for i in entries:
        print(i)

def deleteEntry(datas):
    originalLen = len(datas)
    name = input("What is the name of the entry you would like to delete?\n")
    datas = [data for data in datas if data["name"] != name]

    if len(datas) == originalLen:
        raise ValueError(f"No item found with name {name}")
    
    return datas

def traitHandler(job, ExisTraits = None):
    itemTraits = {"Metal":"Has the qualities of metal, including greater durability and susceptibility to rust and electricity.",
                 "Fragile":"Fragile items have 1/2 the normal durability.",
                 "Starter":"Starter items are able to be acquired at the start of the game.",
                 "Rust":"Rusty items automatically gain the Fragile trait, but deal extra poison damage on a hit.",
                 "Blessed": "Blessed weapons deal extra holy damage, which has extra effect on unholy creatures and no effect on holy creatures."}
    npcTraits = {}
    equippableTraits = {}
    traits = []

    if job == 'create':
        done = False
        if ExisTraits:
            print(f"The current traits are {ExisTraits}")
        print("Please enter the traits you would like to give this item.")
        while not done:
            trait = input("(Enter N when you're done, or T to see all current traits)\nEnter Trait: ")
            if trait == "N" or trait == 'n':
                done = True
            elif trait == "T" or trait == 't':
                category = input("Would you like to see the [I]tem traits, [N]pc traits, or [E]quipable traits?\n").lower()
                if category == 'i':
                    print(itemTraits)
                elif category == 'n':
                    print(npcTraits)
                elif category == 'e':
                    print(equippableTraits)
                else:
                    print("None of those were an option. Please try again.")
            else:
                traits.append(trait)
        if "Rust" in traits and "Fragile" not in traits:
            traits.append("Fragile")
        if ExisTraits:
            ExisTraits.extend(traits)
            return ExisTraits
        else:
            return traits
    
    if job == 'remove':
        done = False
        while not done:
            print(f"The current traits for this item are {ExisTraits}")
            deleted = input("What trait would you like to remove? (Type 'ALL' for all)  ")
            if deleted in ExisTraits:
                ExisTraits.remove(deleted)
                print(f"The {deleted} trait has been removed.")
            elif deleted == "ALL":
                ExisTraits = []
            else:
                print(f"Sorry, but {deleted} is not in the traits for this item. Please try again.")
                continue
            moreToDo = input("Would you like to delete more entries, y or n?   ").lower()
            if moreToDo == 'n':
                done = True
        return ExisTraits

def addEntry(datas, category):
    entryName = input("What is the name of the entry you would like to make?\n")

    for i in datas:
        if i["name"] == entryName:
            print(f"Item with name {entryName} already exists. Moving to Alter Entry...")
            changeEntry(datas)
            break
    if category == 'item':
        name = entryName
        traits = traitHandler('create')
        weight = float(input("Input weight: "))
        price = float(input("Input price in Silver Pieces: "))

        newEntry = {"name":name,"traits":traits,"weight":weight,"price":price}
        datas.append(newEntry)
        return datas

    elif category == 'npc':
        "Temp"
    elif category == 'enemy':
        "Temp"
    else:
        print("It shouldn't be possible to see this error message...")

def changeEntry(datas):
    readAllEntries(datas)
    choice = input("What entry would you like to modify?\nQ to quit")
    if choice.lower() == 'q':
        print("Exiting Application...")
        sys.exit()
    if "1" in choice or "2" in choice or "3" in choice or "4" in choice or "5" in choice or "6" in choice or "7" in choice or "8" in choice or "9" in choice or "0" in choice:
        choice = int(choice)
    for data in datas:
        if data["name"] == choice or data["id"] == choice:
            willContinue = True
            while willContinue:
                print(data)
                chosenKey = input("Enter N to quit\nSelect key to edit: ")
                if chosenKey == "N" or chosenKey == 'n':
                    willContinue = False
                elif chosenKey == "traits":
                    traits = data["traits"]
                    subsection = input("Would you like to [a]dd new traits, [d]elete some traits, or [b]oth?\nQ to quit   ").lower()
                    if subsection == "q":
                        print("Exiting Application...")
                        sys.exit()
                    if subsection == 'a':
                        traits = traitHandler('create', traits)
                    elif subsection == 'd':
                        traits = traitHandler('remove', traits)
                    elif subsection == 'b':
                        traits = traitHandler('create', traits)
                        traits = traitHandler('remove', traits)
                    else:
                        print("That's not a valid option. Please try again.")
                        continue
                    data['traits'] = traits
                else:
                    newValue = input("What do you want to change the key to?\nPress Q to quit\n")
                    if newValue == 'q' or newValue == "Q":
                        print("Exiting Application...")
                        sys.exit()
                    try:
                        data[chosenKey] = newValue
                    except:
                        print(f"{chosenKey} is not a trait of {data}")


def itemWriter():
    filename = './items.json'
    continueEdit = True
    if not os.path.isfile(filename):
        with open(filename,'w') as file:
            json.dump([], file)
    while continueEdit:
        with open(filename,'r') as file:
            data = json.load(file)
            action = input("Would you like to [D]elete an entry, [A]lter an existing entry, [C]reate a new entry, or [M]ove to a different directory?\n").lower()
            if action == 'd':
                readAllEntries(data)
                data = deleteEntry(data)
                with open(filename, 'w') as file:
                    json.dump(data,file,indent=4)
            elif action == 'm':
                continueEdit = False
            elif action == 'c':
                data = addEntry(data, 'item')
                with open(filename,'w') as file:
                    json.dump(data, file, indent=4)
            elif action == 'a':
                changeEntry(data)
                with open(filename, 'w') as file:
                    json.dump(data,file,indent=4)
            else:
                print("That's not a valid action.")
        

def npcWriter():
    continueEdit = True
    while continueEdit:
        action = input("Would you like to [D]elete an entry, [M]odify an existing entry, or [C]reate a new entry?\n").lower()

def enemyWriter():
    continueEdit = True
    while continueEdit:
        action = input("Would you like to [D]elete an entry, [M]odify an existing entry, or [C]reate a new entry?\n").lower()

def main():
    while True:
        whichList = input("Would you like to edit the [I]tems, [N]pcs, or [E]nemies?\nQ to quit\n").lower()
        if whichList == 'i' or whichList == 'items' or whichList == 'item':
            itemWriter()
        elif whichList == 'n' or whichList == 'npcs' or whichList == 'npc':
            npcWriter()
        elif whichList == 'e' or whichList == 'enemies' or whichList == 'enemy':
            enemyWriter()
        elif whichList == 'q':
            print("Exiting Application...")
            sys.exit()
        else:
            print("Invalid input, try again.")
            continue

if __name__ == "__main__":
    main()