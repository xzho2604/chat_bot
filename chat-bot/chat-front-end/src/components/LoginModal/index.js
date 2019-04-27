import React from 'react';
import { Modal, Button } from 'antd';
import "antd/dist/antd.css";
import "./LoginModal.css";
import { faceLogin } from "../../apis";
import { canvasHeight, canvasWidth} from "../../config";

class LoginModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            modalVisible: false,
            modalLoading: false,
            stat: null,
            title: "Please login"
        };
        this.videoRef = React.createRef();
        this.canvasRef = React.createRef();
    }

    componentDidMount = () => {
        this.setModalVisible(true);
    };

    handleOK = () =>  {
        console.log("Ok");
    };

    setModalVisible(modalVisible) {
        this.setState({ modalVisible });
        this.setState({stat: "Capture"});
        this.openCam();
    }

    handleLoginSuccess = (res) => {
        let { user } = JSON.parse(res.data);
        // let { user } = res.data;
        this.setState({ modalLoading: false, modalVisible: false });
        setTimeout(() => this.props.callback(user), 500);
    };

    handleLoginError = (err) => {
        this.setState({
            modalLoading: false,
            modalVisible: true,
            stat: "Capture",
            title: "Can't recognize you, please place your face in the center area." });
        alert("Login failed");
        console.error(err);
    };

    handleSubmit = () => {
        this.closeCam();
        this.setState({ modalLoading: true });
        let data = this.canvasRef.current.getContext('2d')
            .getImageData(0, 0, canvasWidth, canvasHeight).data;
        faceLogin(data, this.handleLoginSuccess, this.handleLoginError);
    };

    handleCancel = () => {
        this.closeCam();
        this.setState({ modalVisible: false });
    };

    handleCapture = () => {
        let canvas = this.canvasRef.current;
        let video = this.videoRef.current;
        canvas.height = canvasHeight;
        canvas.width = canvasWidth;
        canvas.getContext('2d').drawImage(video, 0, 0, canvasWidth, canvasHeight);
        this.closeCam();
        this.setState( {stat: "Submit"});
    };

    handleRetake = () => {
        this.openCam();
        this.setState( {stat: "Capture"});
    };

    closeCam = () => {
        let video = this.videoRef.current;
        video.srcObject.getTracks()[0].stop();
    };

    openCam = () => {
        //Only works with the newest api
        navigator.mediaDevices.getUserMedia({
            audio: false,
            video: { width: 400, height: 300 }
        }).then(function(stream) {
                /* use the stream */
                let video = this.videoRef.current;
                this.setState({video: video});
                video.srcObject = stream;
                video.play();
            }.bind(this))
            .catch(function(err) {
                /* TODO pass the user without cam by. */
                this.props.callback("Test User");
                alert("You need a camera to login. But I'll log you in in this test mode.");
                console.error(`Error: ${err.name}, ${err.message}`);
            }.bind(this));
    };

    render() {
        const { modalVisible, modalLoading } = this.state;
        const footer = {
            "Submit": [
                <Button key="backBtn" onClick={this.handleRetake}>Retake</Button>,
                <Button key="captureBtn" type="primary" loading={modalLoading} onClick={this.handleSubmit}>
                    Submit
                </Button>,
            ],
            "Capture": [
                //<Button key="cancelBtn" onClick={this.handleCancel}>Cancel</Button>,
                <Button key="submitBtn" type="primary" onClick={this.handleCapture}>
                    Capture
                </Button>,
            ],
            // "Form": [
            //     <Button key="cancelBtn" onClick={this.handleCancel}>Cancel</Button>,
            //     <Button key="submitBtn" type="primary" onClick={this.handleCapture}>
            //         Face Login
            //     </Button>,
            // ]
        };

        return (
            <div>
                <Modal
                    visible={modalVisible}
                    title={this.state.title}
                    style={{ top: 20 }}
                    onOk={this.handleOK}
                    onCancel={this.handleCancel}
                    footer={footer[this.state.stat]}
                >
                    <video id="video" ref={this.videoRef} className={this.state.stat}/>
                    <canvas id="canvas" ref={this.canvasRef} className={this.state.stat}/>,
                </Modal>
            </div>
        );
    }
}

export default LoginModal;
