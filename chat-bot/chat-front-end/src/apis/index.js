import axios from 'axios';
import { backEndUrl } from '../config';
const backEnd = axios.create({
    baseURL: backEndUrl
});
export const backEndLoginApi = (payload, success, err) => {
    backEnd.post('login', payload)
        .then(success)
        .catch(err);
};

export const backEndDataApi = (payload, success, err) => {
    backEnd.post('', payload)
        .then(success)
        .catch(err);
};

// axios.post(config.backEndApi, {
//     params: messageObject
// }).then(res => {
//         console.log(res);
//         let r = JSON.parse(res.data);
//         if (r.type === 'text') {
//             addResponseMessage(r.res);
//         } else {
//             renderCustomComponent(
//                 itemDict[r.type], r.payload, true
//             )
//         }
//     });
//