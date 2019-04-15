import React from 'react';
import testSvg from './weatherIcons/wi-cloud.svg'
import './WeatherComponent.css';
import { Cities } from './Cities';
const weatherItem = (weatherItem) => {
    return (
        <div className="container" style={{backgroundImage : `url(${Cities[weatherItem.city]})`}}>
            <h1 className="title">{weatherItem.title}</h1>
            <div className="left">
                <h3 className="city">{weatherItem.city}</h3>
                <div className="Temp">{weatherItem.temp}</div>
            </div>
            <div className="right">
                {/*<div className="icon">This is an icon</div>*/}
                <img src={testSvg} alt="test" />
            </div>
        </div>
    );

    /*
     *    UI container: width: 30em; height: 10em; background:linear-gradient(to right, red, pink); border-radius: 10px
     *    title: text-align: center
     *    left:
     */


};

export default weatherItem;