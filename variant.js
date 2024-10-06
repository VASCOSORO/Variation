const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client();

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Escaneá este código QR para conectarte a WhatsApp');
});

client.on('ready', () => {
    console.log('WhatsApp Web está conectado.');
});

client.on('message', message => {
    console.log(`Mensaje recibido de ${message.from}: ${message.body}`);
    if (message.body === 'Hola') {
        message.reply('¡Hola! ¿Cómo puedo ayudarte?');
    }
});

client.initialize();

