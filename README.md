
# CodeIT Suisse 2022 Entry Challenge

____________________________________________________________________________________________________________________________________________________________________

# Team Members:-

* _Team Name:_ **NameError**
  <br />
  <br />
* _Name:_ Masood Ahmed
  <br />
  _Email:_ masood20@connect.hku.hk
  <br />
  _Alternate Email:_ mangimasood2000@gmail.com
  <br />
  _GitHub Username:_ @Masood-Ahmed271
  <br />
  <br />

* _Name:_ Abdulwadood Ashraf Faazli
  <br />
  _Email:_ awaf2001@connect.hku.hk
  <br />
   _Alternate Email:_ abwadood01@gmail.com
  <br />
  _GitHub Username:_ @abdulwadoodfaazli
  <br />
  <br />

* _Name:_ Ryan Judistira Gani
  <br />
  _Email:_ ryanjgani@gmail.com
  <br />
   _Alternate Email:_ ryanscar9@gmail.com
  <br />
  _GitHub Username:_ @ryanjgani
  <br />
  <br />
  
___________________________________________________________________________________________________________________________________________________________________
  
# Problem Description
  
## Input:
  
  A comma-separated-value (CSV) stream of ticks in the format: <br />
  
  `timestamp, ticker, quantity, price`
  <br />

  For this challenge:
  * Time stamp will be in hh:mm which can be treated as a string
  * Price would be any positive float value greater than 0.0, only 1 decimal place is needed to be handled

  <br />

## Part One:

  Aggregate the stream by time in chronological order, with each output record in the format:
  <br /><br />
  `timestamp, ticker1, cumulative_quantity1, cumulative_notional1, ticker2, cumulative_quantity2, cumulative_notional2 , ......`

  <br />
  Example: 00:00,A,5,5.5,B,4,4.4
  <br />

  <br />
  The group ticker, cumulative_quantity, cumulative_notional repeats for each ticker with a tick at the timestamp. Tickers should be sorted alphabetically as well. 
<br /><br />
The notional is the product of quantity and price at each tick, and the cumulative_notional is the running sum of notional values for each ticker up till the timestamp.
<br /><br />

The implementation should be done in a to_cumulative function (or equivalent) that takes in a list of strings, and returns a list of strings.    
<br />

## Part Two:
  
Aggregate the stream by time in chronological order, but this time each output record is 'delayed' by only reporting cumulative quantities in blocks of quantity_block.

Take note that if only a portion of the current tick is applied for reporting the quantity blocks, the notional calculation should factor the correct quantity, with the leftover quantity effectively 'hidden' from the true cumulative_notional.

The implementation should be done in a to_cumulative_delayed function ( or equivalent ) that takes in a list of strings and an integer, and returns a list of strings.


**Example:** 

quantity_block: 5

Input: 
[
    "00:06,A,1,5.6",
    "00:05,A,1,5.6",
    "00:00,A,1,5.6",
    "00:02,A,1,5.6",
    "00:03,A,1,5.6",
    "00:04,A,1,5.6"
  ]

  Result:
  [
    "00:05,A,5,28.0"
  ]

  "00:06,A,1,5.6" is not included in the output as the cumulative quantity is not a multiple of 
  quantity_block which is 5 in this case.


## Assumptions:

* Assumption 1: The input is just some static data which is fed only once. It is not a live stream of data.
* Assumption 2: The tickers are always uppercase letters
* Assumption 3: The time stamps are all in 24 hour clock format
* Assumption 4: The stream has data only spanning 24 hours
* Assumption 5: The timestamp, ticker, quantity, price will always be available in each ticker and we won't be getting empty values


____________________________________________________________________________________________________________________________________________________________________

