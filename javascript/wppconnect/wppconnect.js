const wppconnect = require('@wppconnect-team/wppconnect');

    wppconnect.create({
        session: 'hore',
    })
        .then((client) => start(client))
        .catch((error) => console.log(error));

    function start(client) {

        const message = 'Halo gaes, ini pesan otomatis'
        const contacts = [
            { name: 'dono', number: '62812345678910', message },
            { name: 'kasino', number: '62812345678911', message },
            { name: 'indro', number: '62812345678912', message },
            { name: 'radit', number: '62812345678913', message },
            { name: 'dika', number: '62812345678914', message },
            { name: 'panji', number: '62812345678915', message },
        ]

        function delayExec(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        async function sendMessagesWithDelay() {
            for (const contact of contacts) {
                console.log('Kirim ke:', contact.name);
                try {
                    await client.sendText(contact.number, contact.message);
                    console.log('Result: success');
                } catch (error) {
                    console.log(`Failed to send message to ${contact.name}:`, error);
                }
                await delayExec(1000); // Wait 1 second before sending the next message
            }
        }

        sendMessagesWithDelay()
    }