import React, { Component } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';
import logo from '../img/UNSW.png';
class App extends Component {
    componentDidMount() {
        addResponseMessage("Hello! I'm your household butler, how can I help you?");
    }

    handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        // TODO insert codes here to fetch data from backend service apis.
        addResponseMessage(newMessage);
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