# [v2.currencything.com](http://v2.currencything.com/) 🤡

![banner](https://i.imgur.com/C5xIPAU.jpg)
This is a colourful and fun **Blockchain Explorer** tracking my discord-based cryptocurrency [Currency Thing](https://sam.freelancepolice.org/discord_bots/currencything).

## Main features
- Displays the entire blockchain as a table, sort-able by any field
- Always up-to-date with the discord blockchain
- Displays key statistics about Currency Thing usage, filterable by time period
- Each statistic is accompanied by a graph
- Highlights milestones transactions (every 1000<sup>th</sup> currency thing minted)
- Fun cursors, sound effects, and wacky design 🤡
   
![blockchain](https://i.imgur.com/O5dn5iJ.jpg)

## User Pages
You can click on any user's name in the blockchain to go their Currency Thing page.
This displays the same type of information as the homepage, but specific to the current user. User statistics and graphs are updated in real-time.

![enter image description here](https://i.imgur.com/oA8DHn7.jpg)

## How it was made
The **backend API** is powered by *Python Flask*, and all the data reading and processing is done with *Pandas*. The graphs are generated with *Matplotlib* as SVGs. The actual blockchain data comes from my *[Currency Thing Discord bot](https://github.com/SamTF/CurrencyThing)*.

The **frontend UI** is powered by *SvelteKit*, making use of both server-side rendering and client-side interactivity and data fetching. The original currencything.com was entirely rendered server-side with Flask, so I decided to rebuild it with SvelteKit to be more interactive, such as allowing for sorting the blockchain headers. SvelteKit also makes the website much faster and snappier than Flask!

The **styling CSS** was done entirely "by hand" using *Sass*. The Clown Logo was designed by me in Illustrator, and the emotes are from my Discord server.

![interactive stats](https://i.imgur.com/LAX3Iva.gif)

## Impressed? Need someone like me?
Offer me a job :)
sebastiancc.info@gmail.com

or check out the rest of my projects on [my personal website](https://sam.freelancepolice.org/).

![me :)](https://sam.freelancepolice.org/static/images/logo.webp)
