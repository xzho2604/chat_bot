import React from 'react';
import './WeatherComponent.css';
import { Cities, Weathers } from './WeatherMap';
const weatherItem = (weatherItem) => {
    let image = Cities[weatherItem.city.toLowerCase()]
        ? Cities[weatherItem.city.toLowerCase()]
        : Cities['Default'];

    let icon = Weathers[weatherItem.weather]
        ? Weathers[weatherItem.weather]
        : Weathers['Default'];

    return (
        <div className="container weather" style={{backgroundImage : `url(${image})`}}>
            <div className="info">
                <h1 className="city">{weatherItem.city}</h1>
                <h2 className="date">{weatherItem.day + ' ' + weatherItem.time}</h2>
                <h1 className="Temp">{weatherItem.temp + '°'}</h1>
            </div>
            <div className="right">
                <object id="mySVG"  aria-label="weatherIcon" data={icon} type="image/svg+xml"/>
                <h3 className="textWeather">{weatherItem.weather}</h3>
            </div>
        </div>
    );
};

export default weatherItem;