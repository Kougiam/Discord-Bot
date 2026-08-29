`cogs/tickets.py`: `TICKET_CATEGORY_ID`, `SUPPORT_ROLE_ID`
- `cogs/autorole.py`: `WELCOME_ROLE_ID`, `WELCOME_CHANNEL_ID`
- `cogs/security.py`: `SECURITY_LOG_CHANNEL_ID`, `ANTI_LINK_EXEMPT_ROLE_IDS`, `ANTI_LINK_EXEMPT_CHANNEL_IDS`, `MIN_ACCOUNT_AGE_DAYS`, `ANTI_ALT_ACTION` (`"kick"` ή `"alert"`)
- `cogs/logging_cog.py`: `LOG_CHANNEL_ID`
- `cogs/leveling.py`: `LEVEL_UP_CHANNEL_ID`

- - Scopes: `bot`, `applications.commands`
- - Bot Permissions: `Administrator` or
     `Kick Members, Ban Members, Moderate Members, Manage Channels, Manage Roles, Manage Messages, Send Messages, Read Message History, View Channels`

Privileged Gateway Intents:
   - `SERVER MEMBERS INTENT`
   - `MESSAGE CONTENT INTENT`

   - !kick
   - !mute
   - !warn
   - !ban @user reason
   - !unban <user_id>
