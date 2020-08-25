const fs = require('fs');
const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
  if (msg.content == 'ping') {
    console.log(`Message from ${msg.author.username}`);
    msg.channel.send('pong');
  }
});

lenin wuz here

let tok = fs.readFileSync('token.txt').toString();
tok = tok.substring(0, tok.length - 1);
client.login(tok);

