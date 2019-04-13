import React from 'react';
import { Modal, Button } from 'antd';
import "antd/dist/antd.css";
// import "./index.css";
import axios from 'axios';

// import { getUserMedia, camSuccess, camError } from "./functions/getCamera";

class LoginModal extends React.Component {
    state = {
        modalVisible: false,
        modalLoading: false,
        stat: null,
        capturedImg: null,
    };

    setModalVisible(modalVisible) {
        this.setState({ modalVisible });
        this.setState({stat: "Capture"});
        this.openCam();
    }

    handleSubmit = () => {
        this.closeCam();
        this.setState({ modalLoading: true });
        //change setTimeOut to submit
        setTimeout(() => {
            this.setState({ modalLoading: false, modalVisible: false });
        }, 3000);
        console.log("Submitting!");

    };

    handleCancel = () => {
        this.setState({ modalVisible: false });
        this.closeCam();
    };

    handleCapture = () => {
        this.closeCam();
        this.setState( {stat: "Submit"});
        let canvas = document.getElementById('canvas');
        let video = document.getElementById('video');
        canvas.height = 360;
        canvas.width = 480;
        canvas.getContext('2d').drawImage(video, 0, 0, 480, 360);
        console.log("Captured!");
    };

    handleRetake = () => {
        this.openCam();
        this.setState( {stat: "Capture"});
        console.log("Retaking!");
    };

    closeCam = () => {
        let video = document.getElementById('video');
        video.srcObject.getTracks()[0].stop();
    };

    openCam = () => {
        //Only works with the newest api
        navigator.mediaDevices.getUserMedia({
            audio: false,
            video: { width: 400, height: 300 }
        })
            .then(function(stream) {
                /* use the stream */
                let video = document.getElementById('video');
                this.setState({video: video});
                video.srcObject = stream;
                video.play();
            }.bind(this))
            .catch(function(err) {
                /* handle the error */
                alert("You don't have a camera, you foo!");
                console.log(`Error: ${err.name}, ${err.message}`);
            });
    };

    render() {
        const { modalVisible, modalLoading } = this.state;
        const videoStyle = {
            "Capture": {margin: "auto", display: "block", borderRadius: "10px"},
            "Submit": {display: "none"},
        };
        const canvasStyle = {
            "Capture": {display: "none"},
            "Submit": {margin: "auto", display: "block"},
        };
        const footer = {
            "Submit": [
                <Button key="backBtn" onClick={this.handleRetake}>Retake</Button>,
                <Button key="captureBtn" type="primary" loading={modalLoading} onClick={this.handleSubmit}>
                    Submit
                </Button>,
            ],
            "Capture": [
                <Button key="cancelBtn" onClick={this.handleCancel}>Cancel</Button>,
                <Button key="submitBtn" type="primary" onClick={this.handleCapture}>
                    Capture
                </Button>,
            ]
        };

        return (
            <div>
                <Button type="primary" onClick={() => this.setModalVisible(true)}>
                    Login
                </Button>
                <Modal
                    visible={modalVisible}
                    title="Please place your face in the center area"
                    style={{ top: 20 }}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    footer={footer[this.state.stat]}
                    onLoad={() => {
                        console.log("loaded.");
                    }}
                >

                    <video id="video" style={videoStyle[this.state.stat]}/>
                    <canvas id="canvas" style={canvasStyle[this.state.stat]}/>,
                </Modal>
            </div>
        );
    }
}

export default LoginModal;