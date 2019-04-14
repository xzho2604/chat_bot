import React, {Component} from 'react';
import {Widget, addResponseMessage, addLinkSnippet, renderCustomComponent, senderPlaceHolder, toggleInputDisabled} from 'react-chat-widget';
// import ReactDOM from 'react-dom';
import 'react-chat-widget/lib/styles.css';
import logo from '../img/UNSW.png';
import VideoItem from './VideoComponent';
import MusicItem from './MusicComponent';
import WeatherItem from './WeatherComponent';
import LoginItem from './LoginItem';
import LoginModal from './LoginModal';
import {messageTester} from '../testItems'
import {chatApi} from '../apis';
import {ObjectID} from "bson";

class App extends Component {
    state = {
        user: null
    };

    componentDidMount = () => {
        toggleInputDisabled();
        addResponseMessage("Hello! I'm a household butler, how can I help you?");
        setTimeout(() => {
            renderCustomComponent(
                LoginModal, [this.loginModalCallback], true);
        }, 1000);
        console.log(process.argv);
    };

    loginModalCallback = (user) => {
        if (user !== null) {
            this.setState({user: user});
            // ReactDOM.unmountComponentAtNode(this.modalRef.current);
            addResponseMessage(`Hello ${user}! How can I help you?`);
            //Enable input
            toggleInputDisabled();
            this.itemDict = {
                music: MusicItem,
                video: VideoItem,
                weather: WeatherItem,
                login: LoginItem
            };
        } else {
            addResponseMessage(`Sorry I can't recognize you, would you like to login manually?`);
            renderCustomComponent(
                LoginItem, null, true
            );
        }
    };

    handleChatSuccess = (r) => {
        console.log(r.data);
        let {type, res, ObjectID } = r.data;
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
            ObjectId: new ObjectID().toString(),
            msg: message,
            timeStamp: new Date(),
            user: this.state.user
        };
        messageTester(message);
        // TODO Test new api.
        // chatApi(payload, this.handleChatSuccess, this.handleChatErr);
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
