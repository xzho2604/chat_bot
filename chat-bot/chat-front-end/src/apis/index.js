import axios from 'axios';
import { canvasWidth, canvasHeight, loginUrl, chatUrl } from '../config';
const chat = axios.create({
    baseURL: chatUrl,
    headers: {
        "Access-Control-Allow-Origin": chatUrl,
        "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token, Accept",
    }
});

const login = axios.create({
    baseURL: loginUrl,
    headers: {
        "Access-Control-Allow-Origin": loginUrl,
        "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token, Accept",
    }
});

const loginApi = (payload, success, error) => {
    login.post('', payload)
        .then(success)
        .catch(error);
};

export const faceLogin = (data, success, error) => {
    let r = [];
    let g = [];
    let b = [];
    for(let i = 0; i < data.length; i += 4) {
        r.push(data[i]);
        g.push(data[i+1]);
        b.push(data[i+2]);
    }
    // convert the image in canvas to r,g,b matrix and send it to login server.
    let formData = new FormData();
    formData.append('height', canvasHeight);
    formData.append('width', canvasWidth);
    formData.append('r', JSON.stringify(r));
    formData.append('g', JSON.stringify(g));
    formData.append('b', JSON.stringify(b));
    loginApi(formData, success, error);
};

export const chatApi = (payload, success, error) => {
    chat.post('', {params: payload})
        .then(success)
        .catch(error);
};

export const backLoginApi = (payload, success, error) => {
    chat.post('/login', {params: payload})
        .then(success)
        .catch(error);
};

export const backLogoutApi = (payload, success, error) => {
    chat.post('/logout', {params: payload})
        .then(success)
        .catch(error);
};