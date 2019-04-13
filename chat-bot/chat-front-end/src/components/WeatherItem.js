import React from 'react';
import testSvg from '../icons/weather-icons-master/svg/wi-cloud.svg'

const weatherItem = (weatherItem) => {
    let item = {
        city: "Sydney",
        title: "Weather Forecast",
        temp: '26°',
        weather: "Sunny"
    };
    return (
        <div className="UI Container" style={{width: "30em", height: "10em", background:"linear-gradient(to right, #00a1ff, #c0e5ff)", borderRadius: "10px"}}>
            <h1 className="title" style={{textAlign: "center", fontFamily: "Georgia", color: "#ffe0e0"}}>{item.title}</h1>
            <div className="left" style={{float: "left", padding: "10px"}}>
                <h3 className="city" style={{color: "white"}}>{item.city}</h3>
                <div className="Temp" style={{color: "white"}}>{item.temp}</div>
            </div>
            <div className="right" style={{float: "right", padding: "10px", width: "80px"}}>
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