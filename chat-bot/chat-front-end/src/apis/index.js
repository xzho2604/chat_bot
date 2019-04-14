import axios from 'axios';
import { backEndUrl } from '../config';
import {ObjectID} from "bson";
const backEnd = axios.create({
    baseURL: backEndUrl,
    headers: {
        "Access-Control-Allow-Origin": backEndUrl,
        "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
    }
});
export const loginApi = (payload, success, err) => {
    backEnd.post('/login', payload)
        .then(success)
        .catch(err);
};

export const chatApi = (payload, success, err) => {
    backEnd.post('', payload)
        .then(success)
        .catch(err);
};