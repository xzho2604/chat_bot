import React, {Component} from 'react';
import {Widget, addResponseMessage, addLinkSnippet, renderCustomComponent, toggleInputDisabled} from 'react-chat-widget';
// import ReactDOM from 'react-dom';
import 'react-chat-widget/lib/styles.css';
import logo from '../img/UNSW.png';
import VideoItem from './VideoComponent';
import MusicItem from './MusicComponent';
import WeatherItem from './WeatherComponent';
import LoginItem from './LoginItem';
import LoginModal from './LoginModal';
import TestLoading from './TestLoading';
// import {messageTester} from '../testItems';
import './App.css';
import {chatApi, backLoginApi, backLogoutApi} from '../apis';
import {ObjectID} from "bson";

class App extends Component {
    state = {
        username: null,
        userID: null
    };

    componentDidMount = () => {
        // const listener = ev => {
        //     ev.preventDefault();
        //     backLogoutApi({'userID': this.state.userID}, null, null);
        //     ev.returnValue='leaving, loging out';
        // };
        // window.addEventListener('beforeunload', listener);

        // toggleInputDisabled();
        //TODO testing
        renderCustomComponent(
            TestLoading, null, true);
        //
        addResponseMessage("Hello! I'm a household butler, how can I help you?");
        setTimeout(() => {
            renderCustomComponent(
                LoginModal, [this.loginModalCallback], true);
        }, 1000);
        console.log(process.argv);

        this.itemDict = {
            music: MusicItem,
            video: VideoItem,
            weather: WeatherItem,
            login: LoginItem
        };
    };

    loginModalCallback = (user) => {
        if (user !== null) {
            this.setState({username: user.userName, userID: user.userID});
            // ReactDOM.unmountComponentAtNode(this.modalRef.current);
            backLoginApi({userID: this.state.userID},
                () => addResponseMessage(`Hello ${this.state.username}! How can I help you?`),
                () => console.error("Login failed"));

            //Enable input
            toggleInputDisabled();
        } else {
            addResponseMessage(`Sorry I can't recognize you, would you like to login manually?`);
            renderCustomComponent(
                LoginItem, null, true
            );
        }
    };

    handleChatSuccess = (r) => {
        console.log(r.data);
        // let {type, res } = JSON.parse(r.data);
        let {type, res} = r.data;
        console.log(type);
        console.log(typeof(res));
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
        console.log(err);
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

export default App;
