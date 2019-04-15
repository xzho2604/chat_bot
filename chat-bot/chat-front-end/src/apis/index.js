import axios from 'axios';
import { backEndUrl, myTestUrl } from '../config';
const backEnd = axios.create({
    // baseURL: backEndUrl,
    baseURL: myTestUrl,
    headers: {
        "Access-Control-Allow-Origin": backEndUrl,
        "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token, Accept",
    }
});
export const loginApi = (payload, success, error) => {
    backEnd.post('/login', payload)
        .then(success)
        .catch(error);
};

export const chatApi = (payload, success, error) => {
    backEnd.post('', payload)
        .then(success)
        .catch(error);
};