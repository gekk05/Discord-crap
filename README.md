# About
Graveyard of random Discord scripts I've written and modified over time as a hobby. Some have legitimate use, some were just for fun. Some work well, some don't. 

## Disc-img

Created to prevent revenge porn from being spread within Discord servers. It can ban images on the fly and inspect all images (message attachments) posted to Discord. Image detection is done primarily though structure similarity comparisons/ orb.

## discord-bridge.py

Originally made as a joke, but it can have some practical use cases. The script uses Discord APIs to monitor events (Discord messages) within specific Discord servers. When a message is received, the bot will use Discord Webhooks to send a copy of the message to a different channel, usually belonging to a different server. Essentially, all of the chat will be transferred, including the Discord avatars, pretty much producing identical messages. 

If someone is annoying, you can add them to ANNOYING_LIST. Any messages from people added to the list will have their messages tRanSlatEd tO sPoNgEbOb TalK.


## channeldel.py

Deletes and remakes a specific Discord channel automatically. Configure this with a cronjob or implement inline event scheduling to run every X hours to avoid server from being TOS'd. 
 
