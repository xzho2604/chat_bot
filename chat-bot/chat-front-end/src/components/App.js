import React, { Component } from 'react';
import { Widget, addResponseMessage, addLinkSnippet, renderCustomComponent } from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';
import logo from '../img/UNSW.png';
import VideoItem from './VideoComponent';
import MusicItem from './MusicComponent';
import WeatherItem from './WeatherItem';
import LoginItem from './LoginItem';
import axios from 'axios';

import backendAPI from '../apis/BackEndApi';
class App extends Component {
    componentDidMount() {
        addResponseMessage("Hello! I'm your household butler, how can I help you?");
        console.log(process.argv);
    }

    handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        let itemDict = {
            music: MusicItem,
            video: VideoItem,
            weather: WeatherItem,
            login: LoginItem
        };
        // TODO insert codes here to fetch data from backend service apis.

        // axios.post('http://localhost:5000/', {
        //     params: {
        //         ObjectID: "TESTID",
        //         query: newMessage
        //     }}).then(res => {
        //         console.log(res);
        //         let r = JSON.parse(res.data);
        //         if (r.type === 'text') {
        //             addResponseMessage(r.res);
        //         }
        //     });

        if (newMessage === 'link') {
            //Render Link
            addResponseMessage("This is a test for link");

            addLinkSnippet( {
                title: 'My awesome link',
                link: 'https://dialogflow.com',
                // target: '_self'
                // target = self for jumping at the same page, target = _blank for jumping in the new page
            });
        } else if (newMessage === 'text') {
            addResponseMessage("This is a test for text");
        } else {
            let item;
            ////////////////////////////////
            //This is a fake data generate part.
            if (newMessage === 'video') {
                //Render Video Item
                addResponseMessage("This is a test for video");
                item = {
                    url: 'https://www.youtube.com/embed/0LHxvxdRnYc'
                };
            }  else if (newMessage === 'music') {
                //Render music item
                addResponseMessage("This is a test for music player.");
                // A tester for music widget
                item = {
                    type: 'album',
                    url: 'https://open.spotify.com/embed/album/1DFixLWuPkv3KT3TnV35m3',
                    title: 'album'
                };
                // item = {
                //     type: "track",
                //     url: "https://open.spotify.com/embed/track/623pmkD6sclgLBQrrPqyz4",
                //     title: 'test'
                // };
            } else if (newMessage === 'weather') {
                addResponseMessage("This is a test for weather widget.");
                item = {
                    time: '16:00 PM 19/01/2019',
                    weather: 'Sunny'
                };
            } else if (newMessage === 'login') {
                addResponseMessage("This is a test for login widget.");
                item = {
                    info: "whatever"
                };
            }
            /////////////////////////////////////////
            renderCustomComponent(
                itemDict[newMessage], item, true
            )
        }
    }

    render() {
        return (
            <div className="App">
                <Widget
                    handleNewUserMessage={this.handleNewUserMessage}
                    profileAvatar={logo}
                    title="COMP9900"
                    subtitle="Team Mr.Robot"
                />
            </div>
        );
    }
}

export default App;
