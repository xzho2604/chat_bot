import React, { Component } from 'react';
import { Widget, addResponseMessage, addLinkSnippet, renderCustomComponent } from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';
import logo from '../img/UNSW.png';
import VideoItem from './VideoComponent';
import MusicItem from './MusicComponent';
import WeatherItem from './WeatherItem';
import LoginItem from './LoginItem';
import LoginModal from './LoginModal';
import { messageTester } from '../testItems'
import { backEndDataApi, backEndLoginApi } from '../apis';
import {ObjectID} from "bson";

class App extends Component {
    state = {
        loggedIn: false
    };

    componentDidMount() {
        addResponseMessage("Hello! I'm a household butler, how can I help you?");
        setTimeout(() => {renderCustomComponent(
            LoginModal, this.handleLogin ,true
        )}, 1500);
        console.log(process.argv);
    }
    
    handleLogin = (user) => {
        if (user !== undefined) {
            addResponseMessage(`Hello ${user}! How can I help you?`);
            this.setState({loggedIn: true});
        } else {
            addResponseMessage(`Sorry I can't recognize you, would you like to login manually?`);
            renderCustomComponent(
                LoginItem, null ,true
            );
        }
    };

    handleDataSuccess = () => {

    };
    handleDataErr = () => {

    };

    handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        // {'ObjectID': object_id, 'res': fullfill_text,'type':action}
        let messageObject = {
            "ObjectID": new ObjectID().toString(),
            "msg": newMessage,
            "timeStamp": new Date()
        };

        console.log(messageObject);
        const itemDict = {
            music: MusicItem,
            video: VideoItem,
            weather: WeatherItem,
            login: LoginItem
        };

        messageTester(newMessage);
        // TODO Test new api.
        // backEndDataApi(messageObject, this.handleDataSuccess, this.handleDataErr);
        };

    render() {
        return (
            <div className="App">
                <Widget
                    handleNewUserMessage={this.handleNewUserMessage}
                    profileAvatar={logo}
                    title="COMP9900"
                    subtitle="Team Mr.Robot"
                    height="300"
                />
            </div>
        );
    }
}

export default App;
