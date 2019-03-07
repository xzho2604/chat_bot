import React, { Component } from 'react';
import { Widget, addResponseMessage, addLinkSnippet, renderCustomComponent } from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';
import logo from '../img/UNSW.png';
import VideoItem from './testVideoComponent';
import MusicItem from './testMusicComponent';
class App extends Component {
    componentDidMount() {
        addResponseMessage("Hello! I'm your household butler, how can I help you?");
    }

    handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        // TODO insert codes here to fetch data from backend service apis.



        if (newMessage === 'video') {
            addResponseMessage("This is a test for video");

            renderCustomComponent(
                VideoItem, null, true
            )
        } else if (newMessage === 'link') {
            addResponseMessage("This is a test for link");

            addLinkSnippet( {
                title: 'My awesome link',
                link: 'https://dialogflow.com',
                // target: '_blank'
            });
        } else if (newMessage === 'music') {
            addResponseMessage("This is a test for music player.");

            renderCustomComponent(
                MusicItem, null, true
            )
        } else {
            addResponseMessage("Simply reply some text.");
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