const fs = require('fs');
const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

const tok = fs.readFileSync('token.txt');
console.log(tok.toString());

console.log('done.');
