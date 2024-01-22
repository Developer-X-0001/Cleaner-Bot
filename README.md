# **Welcome to Cleaner#8788 (v6.3.1 HotFix)**
*An advanced message cleaning utility bot is used to clean a specific amount of messages in a channel. Can delete channels, roles, messages.*

## **Changelog v6.3.1 HotFix:**
- Fixed and updated Clean commands.
  - Removed **pins** and **contains** argument from `/clean bot` and `/clean user` commands.
  - Decreased maximum message deletion amount to **50**.
  - Added 0.5-1.5s and 1.0-2.0s cooldown on `/clean messages` when amount is greater than 10 and 25 respectively.
- Improved Badwords system.
  - Ability to add multiple badwords at once.
  - Added autocomplete function in `/badwords remove` when removing badwords.
- Updated Role delete command.
  - Added a check where the bot will throw error if the mentioned role is higher than the bot or the user's role.
- Added ability to report errors.
  - Whenever a command fails you'll be shown with a button saying **Submit Report!**, pressing it will send it directly to the support server.
- Rewamped the Database system.
- Cooldown for `/nuke` command reduced to **15 days**.
##### For further information use command `/changelog` or `/help`

# **Commands:**
**1. Help:** Shows help page with all commands

------------

### **2. Cleaning Commands:**
These commands can be found under `/clean` command group
- **Clean:** Delete a specified number of messages.
- **User:** Delete a specified of messages sent by the mentioned user.
- **Bot:** Delete a specified number of messages sent by bots.
- **Mass-delete:** Delete someone's messages all across the server not just from the current channel.

------------

### **3. Delete Commands:**
These commands can be found under `/delete` command group
- **Channel:** Delete the mentioned channel.
- **Category:** Delete the mentioned category.
- **Role:** Delete the mentioned role.
- **Thread:** Delete the mentioned thread.
- **Emoji:** Delete the specified emoji.
- **Nickname:** Delete the nickname of the mentioned user set in current server.

------------

### **4. Purge Commands:**
These commands can be found under `/purge` command group
- **Channel:** Deletes and re-creates the mentioned or current channel, with same permissions.
- **Category:** Deletes and re-creates the current category

------------

### **5. Badword Filter Commands:**
These commands can be found under `/badwords` command group
- **Add:** Adds one or multiple words to the blacklist words.
- **List:** Shows all the blacklisted words with their total count.
- **Remove:** Removes a word from the blacklisted words.

------------

### **6. Settings Commands:**
These commands can be found under `/settings` command group
- **Audit Channel:** Set a channel to get message logs.
- **Default Pins:** Set default pinned messages check condition.
- **Default Amount:** Set default cleaning amount for clean message command
- **Reset:** Reset all settings for the current server.
- **Show:** View the current settings for the server.

------------

### **7. Special Commands:**
Following command can be invoked by server owner only.
- **Nuke:** Wipes everything from the server except members, **THIS IS A DANGEROUS COMMAND!**

------------

### **8. Help & Support:**
- **Report:** Facing issues using the bot? submit the report by /report
- **Suggestion:** Want something to get added to bot? Tell us your ideas /suggestion

------------

### **9. Other Commands:**
- **Check Permissions:** Check if the bot has all necessary permisions to work properly
- **News:** Shows latest announcements or news by the developers
- **Changelog:** Shows latest changelog.
- **Ping:** Shows bot current latency.
- **Info:** Shows bot information
- **Help:** Shows this message.

------------

# **Authors:**
### **Developers:**
- **[@developer_x](discordapp.com/users/730108671228510269)**
------------
### **Beta Testers:**
- [@god_of_power](discordapp.com/users/664135339589500929)
- [@lory2007_](discordapp.com/users/604339998312890379)
- [@tomclancy247](discordapp.com/users/784769278531993640)
- [@uidea](discordapp.com/users/1048240605320446012)
- [@nemad](discordapp.com/users/804922651302821939)
- [@itsmeoverhere](discordapp.com/users/447470299169030169)
------------
***For any queries join the [support server](https://discord.gg/C9TN63q7xn "Cleaner Support Server"), and our support assistants will help you out. If you are not satisfied, just drop me a DM ([@developer_x](discordapp.com/users/730108671228510269))***
