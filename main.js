const fs = require('fs');
const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', async () => {
  console.log(`Logged in as ${client.user.tag}!`);
  const ch = await client.channels.fetch('733207005304586272');
  ch.send('Got an update! Reloading bot.');
});

client.on('message', async msg => {
  if (msg.content == 'ping') {
    console.log(`Message from ${msg.author.username}`);
    msg.channel.send('pong');
  }
});

let tok = fs.readFileSync('token.txt').toString();
tok = tok.substring(0, tok.length - 1);
client.login(tok);

