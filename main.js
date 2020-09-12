const fs = require('fs');
const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', async () => {
  console.log(`Logged in as ${client.user.tag}!`);

  client.channels.fetch('754173414867992686').then(ch => {
    console.log(`ch id: ${ch.id}`);
    ch.send('Got an update! Reloading bot.');
  }).catch(err => {
    console.log(err);
  });
});
blyat
client.on('guildMemberAdd', async member => {
  // If the guild isn't PurdueSPS, ignore it
  if (member.guild.id != '481808675346841600') return;

  // Add 'Temporary Member' role
  await member.roles.add('737803642463060048');
  console.log(`Added role Temporary Member to ${member.displayName}`);

  await member.send(`Hey there! Thanks for joining the Purdue SPS server. We're glad to have you.\nIf you wouldn't mind, please change your server nickname to your first and/or last name. If you're having trouble with this, ask one of the administrators for help. Thanks!`);
});

client.on('guildMemberRemove', async member => {
  // If the guild isn't PurdueSPS, ignore it
  if (member.guild.id != '481808675346841600') return;

  const admin_channel = await client.channels.fetch('748038519213260872');
  admin_channel.send(`A person left!\nname: ${member.displayName}\nid: ${member.id}`);
});

client.on('message', async msg => {
  if (msg.content == 'ping') {
    console.log(`Message from ${msg.author.username}`);
    msg.channel.send('pong2');
    return;
  }

  if (msg.content == '!log') {
    if (msg.guild.id != '286028084287635456') return;
    const log = fs.readFileSync('log.txt').toString();
    const lines = log.split('\n');

    longPrint(lines, msg.channel.send);

    // let str = '';
    // for (const l of lines) {
    //   if (str.length + l.length + 1 < 2000) {
    //     str = str + l + '\n';
    //   }
    //   else {
    //     await msg.channel.send(str);
    //     str = l;
    //   }
    // }
    // if (str.length > 0)
    //   await msg.channel.send(str);
    // return;
  }

  // console.log(`Unrecognized shit: ${msg.content}`);
});

let tok = fs.readFileSync('token.txt').toString();
tok = tok.substring(0, tok.length - 1);
client.login(tok);

const longPrint = async (strIn, sendfn) => {
  let str = '';
  for (const l of strIn) {
    if (str.length + l.length + 1 < 2000) {
      str = str + l + '\n';
    }
    else {
      await sendfn(str);
      str = l;
    }
  }
  if (str.length > 0)
    await sendfn(str);
  return;
}

