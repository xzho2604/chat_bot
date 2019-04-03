# Backend 2 Front End Communication API

## Communication protocal
* back end to the front end will return a jasnified string of the form: />
 {'ObjectID': object_id, 'res': fullfill_text,'type':action}  />
where the Object ID is the ID from the front end and res will contain the response data structure , type is the actual action of the intent

## Type
By intention there are currently the following types:
* music.play : for music processing
* weather
* flight.book

# Fullfill_text
The form of the data structure returned in fullfill_text convinient for front end processing
* music.play: 
* weather: {"wed": "scattered clouds", "thu": "light rain", "fri": "scattered clouds", "sat": "light rain", "sun": "clear sky", "city": "Sydney"}
* flight.book: "done flight booking!"
