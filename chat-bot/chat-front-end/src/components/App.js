import React, { Component } from 'react';
import { Widget, addResponseMessage, addLinkSnippet, renderCustomComponent } from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';
import logo from '../img/UNSW.png';
import VideoItem from './VideoComponent';
import MusicItem from './MusicComponent';

import axios from 'axios';

import backendAPI from '../apis/BackEndApi';
class App extends Component {
    componentDidMount() {
        addResponseMessage("Hello! I'm your household butler, how can I help you?");
    }

    handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
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
        // should return the exact objectID as front-end passed.
        // backendAPI.post(':3000', {
        //     params: {
        //         objectID: 'TEST',
        //         query: newMessage
        //     }
        // });
        if (newMessage === 'video') {
            //Render Video Item
            addResponseMessage("This is a test for video");
            let videoItem = {
                url: 'https://www.youtube.com/embed/0LHxvxdRnYc'
            };
            renderCustomComponent(
                VideoItem, videoItem, true
            )
        } else if (newMessage === 'link') {
            //Render Link
            addResponseMessage("This is a test for link");

            addLinkSnippet( {
                title: 'My awesome link',
                link: 'https://dialogflow.com',
                // target: '_blank'
            });
        } else if (newMessage === 'music') {
            //Render music item
            addResponseMessage("This is a test for music player.");
            // A tester for music widget
            let musicInfo = {
                type: 'album',
                url: 'https://open.spotify.com/embed/album/1DFixLWuPkv3KT3TnV35m3',
                title: 'album'
            };
            renderCustomComponent(
                MusicItem, musicInfo, true
            )
        }
    };

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
