import axios from 'axios';

export interface ResponseData {
    state: number;
    link: string;
    price: number;
    reply: string;
    apy: string; // 根据示例，这里假设APY是字符串形式的数字
    symbol: string;
    type: string;
    imgUrl: string;
    protocol: string;
}

export async function postData(userInput: string) {
    console.log('User Input:', userInput);
    const url = 'http://127.0.0.1:5000/request';
    const data = {
        query: userInput,
    };

    try {
        const response = await axios.post<ResponseData>(url, data);
        console.log('response:', response)
        console.log('Status Code:', response.status);
        console.log('Response:', response.data);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error('Error Message:', error.message);
        } else {
            console.error('Unexpected Error:', error);
        }
        throw error;
    }
}
