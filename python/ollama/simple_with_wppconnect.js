// how to run
// cd python/ollama
// node --env-file=../../.env simple_with_wppconnect.js

const wppconnect = require('@wppconnect-team/wppconnect');
const axios = require('axios');
require('dotenv').config();

wppconnect.create({
    session: 'test',
})
    .then((client) => start(client))
    .catch((error) => console.log(error));

function start(client) {
    client.onMessage(async (message) => {
        if (message.from == process.env.TESTING_NO) {
            const payload = {
                message: message.content,
            };
            await client.startTyping(message.from);
            const response = await axios.post('http://127.0.0.1:8000/ai_response/', payload);
            await client.sendText(message.from, response.data)            
            await client.stopTyping(message.from);
        }
    });
}