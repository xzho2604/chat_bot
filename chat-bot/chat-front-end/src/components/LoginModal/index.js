import React from 'react';
import { Modal, Button } from 'antd';
import "antd/dist/antd.css";
import "./LoginModal.css";
import {loginApi} from "../../apis";
// import { getUserMedia, camSuccess, camError } from "./functions/getCamera";
import axios from 'axios';
import {loginUrl} from "../../config";
let canvasHeight = 360;
let canvasWidth  = 480;
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
    // componentDidMount() {
    // }
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
    }
    handleLoginSuccess = (res) => {
        console.log(res.data);
        this.setState({ modalLoading: false, modalVisible: false });
        // this.destoryAll();
        this.props[0](res.data.user);

        // TODO hide the button after loggedIn
        //     if (res.data.user !== null) {
        //         this.modalRef.current.style = {display: "none"};
        //         console.log("Here");
        //     }
    };
    handleLoginError = (err) => {
        console.log(err);
    };

    uploadData = () => {
        let data = this.canvasRef.current.getContext('2d')
            .getImageData(0, 0, canvasWidth, canvasHeight).data;
        let r = [];
        let g = [];
        let b = [];
        for(let i = 0; i < data.length; i += 4) {
            r.push(data[i]);
            g.push(data[i+1]);
            b.push(data[i+2]);
        }
        let formData = new FormData();
        formData.append('height', canvasHeight);
        formData.append('width', canvasWidth);
        formData.append('r', JSON.stringify(r));
        formData.append('g', JSON.stringify(g));
        formData.append('b', JSON.stringify(b));
        loginApi(formData, this.handleLoginSuccess, this.handleLoginError);
    };

    upload = (blob) => {
        console.log(blob);
        let formData = new FormData();
        formData.append('image', blob);
        loginApi(formData, this.handleLoginSuccess, this.handleLoginError);
        // // 图片ajax上传，字段名是image
        // var xhr = new XMLHttpRequest();
        // // 文件上传成功
        // xhr.onload = function() {
        //     // xhr.responseText就是返回的数据
        // };
        // // 开始上传
        // xhr.open('POST', 'upload.php', true);
        // xhr.send(data);
    };
    handleSubmit = () => {
        this.closeCam();
        this.setState({ modalLoading: true });
        this.uploadData();
        // console.log(this.canvasRef.current.getContext('2d'));
        // let imageData = this.canvasRef.current.getContext('2d').getImageData(0, 0, canvasWidth, canvasHeight);
        // let data = imageData.data;
        // let outputData = [];
        // for(let i = 0; i < data.length; i += 4) {
        //     let brightness = 0.34 * data[i] + 0.5 * data[i + 1] + 0.16 * data[i + 2];
        //     outputData.push(brightness);
        // }
        // loginApi({image: outputData}, this.handleLoginSuccess, this.handleLoginError);
        // this.canvasRef.current.toBlob(this.upload);
        // let imgURL = this.canvasRef.current.toBlob((cb) => {
        //     let reader = new FileReader();
        //     reader.addEventListener("loadend", function() {
        //         // reader.result contains the contents of blob as a typed array
        //         console.log(reader.result);
        //     });
        //     reader.readAsArrayBuffer(cb);
        // });

        // console.log(imgURL);
        // loginApi({login: "TEST"}, this.handleLoginSuccess, this.handleLoginError);
        console.log("Submitting!");
    };

    handleCancel = () => {
        this.closeCam();
        this.setState({ modalVisible: false });
    };

    handleCapture = () => {
        this.closeCam();
        this.setState( {stat: "Submit"});
        let canvas = this.canvasRef.current;
        let video = this.videoRef.current;
        canvas.height = canvasHeight;
        canvas.width = canvasWidth;
        canvas.getContext('2d').drawImage(video, 0, 0, canvasWidth, canvasHeight);
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
                console.log("Here");
                this.setModalVisible(true);
                let video = this.videoRef.current;
                this.setState({video: video});
                video.srcObject = stream;
                video.play();
            }.bind(this))
            .catch(function(err) {
                /* handle the error */
                this.props[0]("Poor guy with no cam");
                alert("You don't have a camera, you foo! But I'll still log you in.");
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
                <Button type="primary" onClick={this.openCam}>
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