import React, {Component} from 'react';
import {Widget, addResponseMessage, addLinkSnippet, renderCustomComponent} from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import logo from '../img/UNSW.png';
import VideoItem from './VideoComponent';
import MusicItem from './MusicComponent';
import WeatherItem from './WeatherComponent';
import LoginItem from './LoginItem';
import LoginModal from './LoginModal';
import './App.css';
import {chatApi, backLoginApi, backLogoutApi} from '../apis';
import {ObjectID} from "bson";

class App extends Component {
    state = {
        username: null,
        userID: null,
        phase: 'login'
    };

    componentDidMount = () => {
        // TODO customize alert info
        window.onbeforeunload = (ev) => {
            ev.preventDefault();
            let result = backLogoutApi(this.state.userID);
            console.log(result);
            ev.returnValue='leaving, loging out';
            return "Logged out.";
        };

        // toggleInputDisabled();
        // //TODO testing
        // renderCustomComponent(
        //     TestLoading, null, true);

        this.itemDict = {
            music: MusicItem,
            video: VideoItem,
            weather: WeatherItem,
            login: LoginItem
        };
    };

    loginModalCallback = (user) => {
        if (user !== null) {
            this.setState({username: user.userName, userID: user.userID, phase: 'chat'});
            backLoginApi({userID: this.state.userID},
                () => addResponseMessage(`Hello ${this.state.username}! How can I help you?`),
                () => console.error("Login failed"));
            // Enable input
            // toggleInputDisabled();
        } else {
            // TODO manually login
        }
    };

    handleChatSuccess = (r) => {
        console.log(r.data);
        let { type, res } = JSON.parse(r.data);
        // let {type, res} = r.data;
        if (type === "text") {
            addResponseMessage(res);
        } else if (type === "link") {
            addLinkSnippet(res);
        } else {
            renderCustomComponent(
                this.itemDict[type], res, true
            )
        }
    };

    handleChatErr = (err) => {
        console.error(err);
    };

    handleNewUserMessage = (message) => {
        let payload = {
            queryID: new ObjectID().toString(),
            msg: message,
            timeStamp: new Date(),
            userID: this.state.userID
        };
        chatApi(payload, this.handleChatSuccess, this.handleChatErr);
    };

    render() {
        if (this.state.phase === 'login') {
            return (
                <LoginModal callback={this.loginModalCallback}/>
            )
        } else {
            return (
                <div className="App">
                    <Widget
                        handleNewUserMessage={this.handleNewUserMessage}
                        profileAvatar={logo}
                        titleAvatar={logo}
                        title="COMP9900"
                        subtitle="Team Mr.Robot"
                        height="300"
                        senderPlaceHolder="Hello"
                    />
                </div>
            );
        }
    }
}

export default App;
