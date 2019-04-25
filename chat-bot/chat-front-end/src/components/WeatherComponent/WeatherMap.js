import Sydney from './cityImgs/Sydney.jpg';
import Shanghai from './cityImgs/Shanghai.jpeg';
import Perth from './cityImgs/Perth.jpeg';
import Melbourne from './cityImgs/Melbourne.jpeg';
import Tasmania from './cityImgs/Tasmania.jpeg';
import Tokyo from './cityImgs/Tokyo.jpeg';
import NewYork from './cityImgs/NewYork.jpeg';
import Adelaide from './cityImgs/Adelaide.jpeg';
import Default from './cityImgs/default.jpeg';

import broken_clouds from './weatherIcons/broken_clouds.svg';
import clear from './weatherIcons/clear.svg';
import cloud from './weatherIcons/cloud.svg';
import few_clouds from './weatherIcons/few_clouds.svg';
import haze from './weatherIcons/haze.svg';
import heavy_intensity_rain from './weatherIcons/heavy_intensity_rain.svg';
import light_intensity_drizzle from './weatherIcons/light_intensity_drizzle.svg';
import light_rain from './weatherIcons/light_rain.svg';
import light_snow from './weatherIcons/light_snow.svg';
import mist from './weatherIcons/mist.svg';
import moderate_rain from './weatherIcons/moderate_rain.svg';
import moderate_snow from './weatherIcons/moderate_snow.svg';
import overcast_clouds from './weatherIcons/overcast_clouds.svg';
import proximity_shower_rain from './weatherIcons/proximity_shower_rain.svg';
import rain from './weatherIcons/rain.svg';
import scattered_clouds from './weatherIcons/scattered_clouds.svg';
import snow from './weatherIcons/snow.svg';

export const Cities = {
    sydney: Sydney,
    shanghai: Shanghai,
    perth: Perth,
    melbourne: Melbourne,
    tasmania: Tasmania,
    tokyo: Tokyo,
    'new york': NewYork,
    adelaide: Adelaide,
    Default: Default,
};

export const Weathers = {
    'clear': clear,
    'clouds': cloud,
    'few clouds': few_clouds,
    'scattered clouds': scattered_clouds,
    'overcast clouds': overcast_clouds,
    'broken clouds': broken_clouds,

    'haze': haze,

    'rain': rain,
    'light intensity drizzle': light_intensity_drizzle,
    'light rain': light_rain,
    'moderate rain': moderate_rain,
    'proximity shower rain': proximity_shower_rain,
    'heavy intensity rain': heavy_intensity_rain,

    'snow': snow,
    'light snow': light_snow,
    'moderate snow': moderate_snow,

    'mist': mist,
};