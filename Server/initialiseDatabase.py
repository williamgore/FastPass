#This file exists purely for testing purposes

from tinydb import TinyDB, Query

#loading the database
guests = TinyDB('guests.json')

# Clearing the existing database
guests.truncate()

# SCHEMA
# name     - String  - Name of the guest
# guestID  - Integer -'primary key' (if it were a relational database), this is what the fpClient will send the server
# hasFP    - Integer - current number of fastpasses held by the guest (could allow for additional fastpasses, ie. the two hour rule)
# lastFP   - Time    - the time at which the guest obtained their last fastpass
# currRide - String  - the ride that they currently 

#inserting some entries
guests.insert({'name': 'Leah', 'guestID': 1, 'hasFP': 0,'lastFP': 0, 'currRide': 'Tower of Terror'})
guests.insert({'name': 'Laurel', 'guestID': 2, 'hasFP': 0,'lastFP': 0, 'currRide': 'Cosmic Rewind'})
guests.insert({'name': 'Will', 'guestID': 3, 'hasFP': 0,'lastFP': 0, 'currRide': 'Rock n Roller Coaster'})
guests.insert({'name': 'Dan', 'guestID': 4, 'hasFP': 0,'lastFP': 0, 'currRide': 'Rise of the Resistance'})
guests.insert({'name': 'Signy', 'guestID': 5, 'hasFP': 0,'lastFP': 0, 'currRide': 'Slinky Dog Dash'})
guests.insert({'name': 'Craig', 'guestID': 6, 'hasFP': 0,'lastFP': 0, 'currRide': 'Seven Dwarfs Mine Train'})
guests.insert({'name': 'Ben', 'guestID': 7, 'hasFP': 0,'lastFP': 0, 'currRide': 'Smugglers Run'})
guests.insert({'name': 'George', 'guestID': 8, 'hasFP': 0,'lastFP': 0, 'currRide': "Space Mountain"})
guests.insert({'name': 'Mickey', 'guestID': 9, 'hasFP': 0,'lastFP': 0, 'currRide': "Mickeys Runaway Railway"})
