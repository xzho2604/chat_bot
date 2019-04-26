import React from 'react';
import { Modal, Button } from 'antd';
import "antd/dist/antd.css";
import "./LoginModal.css";
import { faceLogin } from "../../apis";
import { canvasHeight, canvasWidth} from "../../config";

// import { getUserMedia, camSuccess, camError } from "./functions/getCamera";
class LoginModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            modalVisible: false,
            modalLoading: false,
            stat: null,
            capturedImg: null,
        };

        this.videoRef = React.createRef();
        this.canvasRef = React.createRef();
        // this.modalRef = React.createRef();
    }
    handleOK() {
        alert("OK!!");
        console.log("OK");
    };

    // destoryAll = () => {
    //     console.log("DESTORY!!");
    //     Modal.destroyAll();
    // };

    setModalVisible(modalVisible) {
        this.setState({ modalVisible });
        this.setState({stat: "Capture"});
        this.openCam();
    }

    handleLoginSuccess = (res) => {
        console.log(res.data);
        console.log(typeof(res.data));
        let { user } = JSON.parse(res.data);
        // let { user } = res.data;
        console.log(user);
        this.setState({ modalLoading: false, modalVisible: false });
        // this.destoryAll();
        // this.props[0](user);
        this.props.callback(user);
        // TODO hide the button after loggedIn
        // if (res.data.user !== null) {
        //     this.modalRef.current.style = {display: "none"};
        //     console.log("Here");
        // }
    };

    handleLoginError = (err) => {
        console.log(err);
        this.setState({ modalLoading: false, modalVisible: false });
        this.props[0](null);
    };

    handleSubmit = () => {
        this.closeCam();
        this.setState({ modalLoading: true });
        let data = this.canvasRef.current.getContext('2d')
            .getImageData(0, 0, canvasWidth, canvasHeight).data;
        faceLogin(data, this.handleLoginSuccess, this.handleLoginError);
        console.log("Submitting!");
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
        console.log("Captured!");
    };

    handleRetake = () => {
        this.openCam();
        this.setState( {stat: "Capture"});
        console.log("Retaking!");
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
        })
            .then(function(stream) {
                /* use the stream */
                let video = this.videoRef.current;
                this.setState({video: video});
                video.srcObject = stream;
                video.play();
            }.bind(this))
            .catch(function(err) {
                /* handle the error */
                // this.props[0]("Test user");
                this.props.callback("Test User");
                alert("You need a camera to login.");
                console.log(`Error: ${err.name}, ${err.message}`);
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
