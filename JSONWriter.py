"""
Program Name: JSON Writer
Purpose: To easily be able to add items, NPCs, enemies, and more to JSON files.
Author: Isaiah Wegwitz
Last Modified: 01/30/2026
"""
import json
import sys
import os.path

"""
Features I still need to implement:
1. Prevent assigning the same id to multiple things.
2. I need to be able to add more than just weapons to the items.
3. I need to be able to add NPCs and Enemies as well.
4. The ID values should be different ranges depending on if they are an item, NPC, or Enemy, that way there is no overlap.
5. I might consider making it so the traits system is separate, in which case I just make base items, NPCs, and Enemies, and the RPG itself handles the traits. For example, 
    I'd make a sword, then the game would decide if the sword is metal, wood, or stone, if it's fragile, if it's magic, blessed, elemental, all that stuff.
"""
def search(entries,key,searchable):
    for data in entries:
        if data[key] == searchable:
            return True, data["name"]
    return False

def idAssign(entries):
    allIDs = []
    for i in entries:
        allIDs.append(i["id"])
    allIDs.sort()

    startID = 1
    for i in allIDs:
        if i != startID:
            return startID
        startID += 1
    return startID

def readAllEntries(entries):
    sorted_entries = sorted(entries,key=lambda x: x["id"])
    for i in sorted_entries:
        print(i)

def deleteEntry(datas):
    originalLen = len(datas)
    name = input("What is the name of the entry you would like to delete?\nQ to quit\n")
    if name == "q" or name == "Q":
        return None
    try:
        id = int(name)
        datas = [data for data in datas if data["id"] != id]
    except:
        datas = [data for data in datas if data["name"] != name]
        dataType = "string"

    if len(datas) == originalLen and dataType == "string":
        raise ValueError(f"No item found with name {name}")
    elif len(datas) == originalLen:
        raise ValueError(f"No item found with id {id}")
    return datas

def traitHandler(job, ExisTraits = None):
    itemTraits = {"Metal":"Has the qualities of metal, including greater durability and susceptibility to rust and electricity.",
                 "Fragile":"Fragile items have 1/2 the normal durability.",
                 "Starter":"Starter items are able to be acquired at the start of the game.",
                 "Rust":"Rusty items automatically gain the Fragile trait, but deal extra poison damage on a hit.",
                 "Blessed": "Blessed weapons deal extra holy damage, which has extra effect on unholy creatures and no effect on holy creatures.",
                 "Wood":"Has the qualities of wood, including lower durability, but being cheaper, and susceptibility to rot and fire.",
                 "Rot":"Rotten items automatically gain the Fragile trait, but have a chance to inflict a disease on a hit."}
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
        id = idAssign(datas)

        newEntry = {"name":name,"traits":traits,"weight":weight,"price":price, "id":id}
        datas.append(newEntry)
        return datas

    elif category == 'npc':
        "Temp"
    elif category == 'enemy':
        "Temp"
    else:
        print("It shouldn't be possible to see this error message...")

def changeEntry(datas):
    dataType = "string"
    readAllEntries(datas)
    choice = input("What entry would you like to modify?\nQ to quit\n")
    if choice.lower() == 'q':
        return
    if "1" in choice or "2" in choice or "3" in choice or "4" in choice or "5" in choice or "6" in choice or "7" in choice or "8" in choice or "9" in choice or "0" in choice:
        choice = int(choice)
    for data in datas:
        if data["name"] == choice or data["id"] == choice:
            while True:
                print(data)
                chosenKey = input("Select key to edit\n Enter q to Quit:\n")
                if chosenKey == "Q" or chosenKey == 'q':
                    break
                elif chosenKey == "traits":
                    traits = data["traits"]
                    subsection = input("Would you like to [a]dd new traits, [d]elete some traits, or [b]oth?\nQ to quit   ").lower()
                    if subsection == "q":
                        break
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
                elif chosenKey == "id":
                    dataType = "int"
                elif chosenKey == "price" or chosenKey == "weight":
                    dataType = "float"
                newValue = input("What do you want to change the key to?\nPress Q to quit\n")
                if newValue == 'q' or newValue == "Q":
                    break
                if dataType == "int":
                    if chosenKey == "id":
                        noMatch = False
                        while not noMatch:
                            found, result = search(datas,"id",newValue)
                            if found:
                                reply = input(f"ID {newValue} already assigned to {result}. Would you like to [T]ry again or [A]ssign a new ID to {result}?\n")
                                if reply == "T" or reply == "t":
                                    newValue = input("Input new id:\n")
                                elif reply == 'A' or reply == 'a':
                                    newNewValue = input(f"Please input a new ID for {result}.\n")
                                    newFound = search(datas,"id",newNewValue)
                                    if not newFound:
                                        result["id"] = newNewValue
                                    else:
                                        print("Sorry, that ID is also already taken. Please try again.")
                                else:
                                    print("That wasn't one of the options. Let's just try this again...")
                            else:
                                noMatch = True
                    newValue = int(newValue)
                if dataType == "float":
                    newValue = float(newValue)
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
            action = input("Would you like to [D]elete an entry, [A]lter an existing entry, [C]reate a new entry, [M]ove to a different directory, or [Q]uit?\n").lower()
            if action == 'q' or action =='Q':
                return
            if action == 'd' or action == 'D':
                readAllEntries(data)
                data = deleteEntry(data)
                with open(filename, 'w') as file:
                    json.dump(data,file,indent=4)
            elif action == 'm' or action == 'M':
                continueEdit = False
            elif action == 'c' or action == 'C':
                data = addEntry(data, 'item')
                with open(filename,'w') as file:
                    json.dump(data, file, indent=4)
            elif action == 'a' or action == 'A':
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