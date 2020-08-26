const fs = require('fs');
const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', async () => {
  console.log(`Logged in as ${client.user.tag}!`);

  client.channels.fetch('733467857719001158').then(ch => {
    console.log(`ch id: ${ch.id}`);
    ch.send('Got an update! Reloading bot.');
  }).catch(err => {
    console.log(err);
  });
});

client.on('message', async msg => {
  if (msg.content == 'ping') {
    console.log(`Message from ${msg.author.username}`);
    msg.channel.send('pong2');
    return;
  }

  if (msg.content == '!log') {
    const log = fs.readFileSync('log.txt').toString();
    const lines = log.split('\n');

    console.log(lines);

    let str = '';
    for (let l of lines) {
      if (str + l + 1 < 2000) {
        str += l + '\n';
      }
      else {
        await msg.channel.send(str);
        str = l;
      }
    }
    if (str.length != 0)
      await msg.channel.send(str);
    return;
  }

  console.log(`Unrecognized shit: ${msg.content}`);
});

let tok = fs.readFileSync('token.txt').toString();
tok = tok.substring(0, tok.length - 1);
client.login(tok);

