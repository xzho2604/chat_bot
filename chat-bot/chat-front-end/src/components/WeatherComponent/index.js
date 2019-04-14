import React from 'react';
import testSvg from '../../icons/wi-cloud.svg'
import './WeatherComponent.css';
import SYD from './Syd.jpg';
const weatherItem = (weatherItem) => {
    let item = {
        city: "Sydney",
        title: "Weather Forecast",
        temp: '26°',
        weather: "Sunny"
    };
    return (
        <div className="container" style={{backgroundImage : SYD}}>
            <h1 className="title">{item.title}</h1>
            <div className="left">
                <h3 className="city">{item.city}</h3>
                <div className="Temp">{item.temp}</div>
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