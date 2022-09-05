"""
    @Description: CodeIT Suisse 2022 Entry Challenge (Python)
    @Team: NameError
"""

# importing datetime and operator to be used further in the code
from datetime import datetime
from operator import itemgetter


"""
    Aggregating the stream by time in chronological order with each output in the format as below:
    `timestamp, ticker1, cumulative_quantity1, cumulative_notional1, ticker2, cumulative_quantity2, cumulative_notional2 , ......`
    Moreover, tickers are also sorted alphabetically

    @Author: Masood Ahmed

    @type arr: list
    @param ticks: A comma separated stream of ticks in the form of list of strings

    @rtype: list
    @returns: a list of strings representing the aggragated stream of ticks which are sorted as required
"""
def to_cumulative(arr):

    initialArray = []      # An array that is used to make list of lists

    # Converting the input into a list of lists with each thing .i.e. time, ticker,... etc as a separate element 
    for stri in arr:
        obj = stri.split(',')
        # Converting in a time object so that we can sort the input accoridngly
        time = datetime.strptime(obj[0], '%H:%M')
        obj[0] = time.time() 
        initialArray.append(obj)

    # Doing Sorting
    initialArray = sorted(initialArray, key=itemgetter(0))

    # Converting the time object back into string for further processing
    for stri in initialArray:
        stri[0] = stri[0].strftime('%H:%M')


    counter = {}      # a counter hash to take a snapshot of each ticker at each timestamp
    hashTable = {}    # a hashTable to store cumulative values at each time stamp


    # A loop that goes through each object which has been sorted in the initial array and finds quantity and notional value
    for obj in initialArray:
        # This else-if would increment things one by one which we can use later to match with time stamps
        # and would find cumulative values
        if obj[1] not in counter:
            multiple = float(obj[2]) * float(obj[3])
            counter[obj[1]] = [int(obj[2]), multiple]
        else:
            multiple = float(obj[2]) * float(obj[3])
            quantity = counter[obj[1]][0] + int(obj[2])
            notional = counter[obj[1]][1] + multiple
            counter[obj[1]] = [quantity, notional]

        # The following else-if would keep track of time stamps
        # and add time stamps accordingly
        if obj[0] not in hashTable:
            ticker = obj[1]
            hashTable[obj[0]] = [{ticker:[counter[ticker][0],counter[ticker][1]]}]
        else:
            ticker = obj[1]
            inside = False
            for material in hashTable[obj[0]]:
                key = list(material.keys())
                if key[0] == ticker:
                    material[ticker] = [counter[ticker][0], counter[ticker][1]]
                    inside = True
            if inside == False:
                hashTable[obj[0]].append({ticker:[counter[ticker][0],counter[ticker][1]]})

    # this for loop is to convert values in hashTable from [{},{}] this form to [[],[]] so that we can sort
    # according to tickers
    newHash = {}
    for key in hashTable:
        if key not in newHash:
            newHash[key] = []
        final = []
        for item in hashTable[key]:
            new = []
            for key2 in item:
                new.append(key2)
                new.append(item[key2][0])
                new.append(item[key2][1])
            final.append(new)
        # sorting according to tickers
        final = sorted(final, key=itemgetter(0))
        newHash[key] = final


    finalList = []       # A list which will have everything sorted and finalised   
    # finalising 
    for key in newHash:
        subList = []
        subList.append(key)
        for ele in newHash[key]:
            for each in ele:
                if type(each) == float:
                    each = round(each, 1)
                subList.append(str(each))
        finalList.append(subList)

    
    finalList2 = []    # The final list having list of strings as required
    # converting list of lists to list of strings
    for ele in finalList:
        stri = ','.join(ele)
        finalList2.append(stri)
    
    # returning answer
    return finalList2

"""
    Aggregating the stream by time in chronological order with each output is delayed by 
    only reporting the cumulative quantities in blocks of quantities block

    @author: Abdulwadood Ashraf Faazli

    @type ticks: list
    @param ticks: A comma separated stream of ticks in the form of list of strings
    @type qb: int
    @param qb: An integer representing the quantity blocks

    @rtype: list
    @returns: a list of strings representing the aggragated stream of ticks which are delayed by the quantity blocks
"""

def to_cumulative_delayed(ticks, qb):
    # Quantifying variables
    ticks.sort()        # It sorts the list of strings by time

    # Quantifying variables
    all_symbols = {}    # This is a hashmap that keeps tracks of changes as they happen
    final = []          # A list that will contain the final strings
    returnString = ""   # To format things 

    # Looping through each tick and deciding on what to put ot not
    for tick in ticks:
        info = tick.split(",")       # splitting the information in each tick into an array .i.e. ["00:00", "A", "1", "5.6"]
        # Getting the necessary information from the particular tick. Then populating the desired variables and converting them into a relevant type
        timestamp = info[0]          # storing the timestamp
        symbol = info[1]             # storing the ticker symbol
        volume = int(info[2])        # storing the quantity
        price = float(info[3])       # storing the price

        # using try-except block for handling the case for latest tick encountered efficiently
        try:

            # This is a while loop that checks volume one by one and cumulatively adds prices
            while volume > 0:
                all_symbols[symbol]["latest_time"] = timestamp      # Updating latest timestamp encountered
                all_symbols[symbol]["quantity"] += 1                # incrementing the quantity/volume by 1 as we have used it
                all_symbols[symbol]["notional"] += price            # incrementing the notional value by price
                volume -= 1             # Decreasing the volume by 1 so it eventually hits 0 and we can break the loop

                # An if condition that only works if the quantity given is a multiple of quantity_block
                if all_symbols[symbol]["quantity"] % qb == 0:
                    # rounding the notional values to one decimal place as required
                    all_symbols[symbol]["notional"] = round(all_symbols[symbol]["notional"], 1)
                    # formatting the strings as required
                    returnString = all_symbols[symbol]["latest_time"] + ","  + symbol + "," + str(all_symbols[symbol]["quantity"]) + "," + str(all_symbols[symbol]["notional"])
                    # putting the final formatted string in the final list
                    final.append(returnString)        

        except:

            # Setting up the dictionary for keeping track of all tickers encountered as per the designed schema
            all_symbols[symbol] = {
                "latest_time": "",
                "quantity": 0,
                "notional": 0,
            }

            # This is a while loop that checks volume one by one and cumulatively adds prices
            while volume > 0:
                all_symbols[symbol]["latest_time"] = timestamp         # Updating latest timestamp encountered
                all_symbols[symbol]["quantity"] += 1      # incrementing the quantity/volume by 1 as we have used it
                all_symbols[symbol]["notional"] += price        # incrementing the notional value by price
                volume -= 1         # Decreasing the volume by 1 so it eventually hits 0 and we can break the loop

                # An if condition that only works if the quantity given is a multiple of quantity_block
                if all_symbols[symbol]["quantity"] % qb == 0:
                    # rounding the notional values to one decimal place as required
                    all_symbols[symbol]["notional"] = round(all_symbols[symbol]["notional"], 1)
                    # formatting the strings as required
                    returnString = all_symbols[symbol]["latest_time"] + ","  + symbol + "," + str(all_symbols[symbol]["quantity"]) + "," + str(all_symbols[symbol]["notional"])
                    # putting the final formatted string in the final list
                    final.append(returnString)

        
    # returning the final answer
    return final

"""
    A block of code to run the desired functions
"""
if __name__ == "__main__":
    # running replit test cases here


    # Test 0: to_cumulative_with_single_tick
    arr = [
      '00:00,A,5,5.5',
    ]
    newArr = to_cumulative(arr)
    if newArr == [ '00:00,A,5,27.5',]:
        print("Test 0 passed")


    # Test 1: to_cumulative_with_multiple_ticks_for_different_tickers
    arr = [
      '00:00,B,4,4.4',
      '00:00,A,5,5.5',
    ]
    newArr = to_cumulative(arr)
    if newArr == ['00:00,A,5,27.5,B,4,17.6',]:
        print("Test 1 passed")


    # Test 2: to_cumulative_with_multiple_ticks_for_different_tickers
    arr = [
      '00:05,A,1,5.6',
      '00:00,A,1,5.6',
      '00:02,A,1,5.6',
      '00:03,A,1,5.6',
      '00:04,A,1,5.6',
    ]
    quantity_block = 5
    newArr = to_cumulative_delayed(arr, quantity_block)
    if newArr == [ '00:05,A,5,28.0',]:
        print("Test 2 passed")


    # Test 3: to_cumulative_delayed_with_different_tickers
    arr = [
      '00:01,A,5,5.5',
      '00:00,A,4,5.6',
      '00:00,B,5,5.5',
      '00:02,B,4,5.6',
    ]
    quantity_block = 5
    newArr = to_cumulative_delayed(arr, quantity_block)
    if newArr == [ '00:00,B,5,27.5', '00:01,A,5,27.9',]:
        print("Test 3 passed")

    # Test 4: to_cumulative_with_single_tick
    arr = [
      '00:00,A,4,5.5',
    ]
    newArr = to_cumulative(arr)
    if newArr == [ '00:00,A,4,22.0',]:
        print("Test 4 passed")

    # Test 5: to_cumulative_with_single_tick
    arr = [
      '00:00,A,4,5.5',
    ]
    quantity_block = 5
    newArr = to_cumulative_delayed(arr, quantity_block)
    print(newArr)
    if newArr == [ ]:
        print("Test 5 passed")