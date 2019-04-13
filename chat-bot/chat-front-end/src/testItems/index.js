import {addLinkSnippet, addResponseMessage, renderCustomComponent} from "react-chat-widget";
import MusicItem from "../components/MusicComponent";
import VideoItem from "../components/VideoComponent";
import WeatherItem from "../components/WeatherItem";
import LoginItem from "../components/LoginItem";

export const messageTester = (newMessage) => {
    console.log(newMessage);
    if (newMessage === 'link') {
        //Render Link
        addResponseMessage("This is a test for link");
        addLinkSnippet(item[newMessage]);
    } else if (itemDict[newMessage] === undefined) {
        addResponseMessage("This is a test for simple text.");
    } else {
        addResponseMessage("This is a test for " + newMessage);
        console.log(item[newMessage]);
        renderCustomComponent(
            itemDict[newMessage], item[newMessage], true
        )
    }
};

const musicItem = {
    album: {
        type: 'album',
        url: 'https://open.spotify.com/embed/album/1DFixLWuPkv3KT3TnV35m3',
        title: 'test'
    },
    track: {
        type: "track",
        url: "https://open.spotify.com/embed/track/623pmkD6sclgLBQrrPqyz4",
        title: 'test'
    },
    playList: {
        type: "list",
        url: "https://open.spotify.com/embed/user/312ki6j7v2dszfilzkihtjiikubu/playlist/151wcXQQc4ZtC9MtssJ7tS",
        title: 'test'
    }
};
const videoItem = {
    url: 'https://www.youtube.com/embed/0LHxvxdRnYc'
};
const weatherItem = {
    time: '16:00 PM 19/01/2019',
    weather: 'Sunny'
};
const loginItem = {
    info: "whatever"
};
const linkItem = {
    title: 'My awesome link',
    link: 'https://dialogflow.com',
    // target: '_self'
    // target = self for jumping at the same page, target = _blank for jumping in the new page
};

const item = {
    "music": musicItem.album,
    "login": loginItem,
    "weather": weatherItem,
    "video": videoItem,
    "link": linkItem
};

const itemDict = {
    music: MusicItem,
    video: VideoItem,
    weather: WeatherItem,
    login: LoginItem
};
