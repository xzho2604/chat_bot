# Backend 2 Front End Communication API

## Communication protocal
where the Object ID is the ID from the front end and res will contain the response data structure , type is the actual action of the intent back end to the front end will return a jasnified string of the form: <br/><br/>
```javascript
 {'ObjectID': object_id, 'res': fullfill_text,'type':action} 
 ```
 <br/>


## Type
By intention there are currently the following types:
* music.play : for music processing
* weather
* flight.book

## Fullfill_text
The form of the data structure returned in fullfill_text convinient for front end processing
*  music.play: <br/>
    * A single song
    ```javascript
    {"type": "track", "contents": [{"name": "Armed And Dangerous","url":"https://open.spotify.com/artist/4MCBfE4596Uoi2O4DtmEMz", "artist_name": "Juice WRLD"}]}
    ```
    * An album <br/>





* weather: 5 day weather forcast including today , city will contain the city being enquired
```javascript
{"wed": "scattered clouds", "thu": "light rain", "fri": "scattered clouds", "sat": "light rain", "sun": "clear sky", "city": "Sydney"}
```
* flight.book: it will be just a confirmation string <br\>
"done flight booking!"
