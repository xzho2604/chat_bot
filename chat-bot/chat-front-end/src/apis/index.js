import axios from 'axios';
import { loginUrl, chatUrl, myTestUrl } from '../config';
const chat = axios.create({
    // baseURL: backEndUrl,
    baseURL: chatUrl,
    headers: {
        "Access-Control-Allow-Origin": chatUrl,
        "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token, Accept",
    }
});
const login = axios.create({
    // baseURL: backEndUrl,
    baseURL: loginUrl,
});

// login.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
login.defaults.headers.post['Access-Control-Allow-Origin'] = loginUrl;
login.defaults.headers.post['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS";
login.defaults.headers.post['Access-Control-Allow-Headers'] = "Origin, Content-Type, X-Auth-Token, Accept";

export const loginApi = (payload, success, error) => {
    login.post('', payload)
        .then(success)
        .catch(error);
};

export const chatApi = (payload, success, error) => {
    chat.post('', payload)
        .then(success)
        .catch(error);
};