start-text =
    Hello 👋
    You can use me to talk to my owner and receive messages from them. Just send any message here!

no =
    { $capitalization ->
       *[lowercase] no
        [capitalized] No
    }

yes =
    { $capitalization ->
       *[lowercase] yes
        [capitalized] Yes
    }

new-topic-intro =
    { $name }
    ├── Has ban: { $ban_status }
    ├── Telegram ID: <code>{ NUMBER($id, useGrouping: 0) }</code>
    ├── Username: { $username }
    ├── Language: { $language_code }
    └── Premium: { $has_premium }


error-cannot-deliver-to-forum =
    Error: couldn't deliver your message to bot owner. Try again in several minutes.

error-cannot-find-user =
    Error: couldn't add corresponding user for this topic. Message not delivered.

error-cannot-deliver-to-forum =
    Error: couldn't deliver your message. Please try again in several minutes.


user-info =
    <b>User info:</b>
    { $user_info }


banned-successfully = User banned successfully. From now on bot will reply to all their messages automatically with ban notification.
shadowbanned-successfully = User shadowbanned successfully. From now on bot will ignore all their messages.

ban-status-ban = ban
ban-status-shadowban = shadowban
ban-status-unknown = unknown

you-are-banned = You were blocked by bot's owner. Your messages will not be delivered.

already-banned = User was already banned before.
already-shadowbanned = User was already shadowbanned before.
already-shadowbanned-before = User is already shadowbanned. There will be not automatic notifications.

any-ban-error = Error while blocking user. Please try again later.

unban-not-needed = User is not banned.
unbanned-successfully = User unbanned successfully.
any-unban-error = Error while unbanning user. Please try again later.

user-info-update-success = User info successfully updated: please check this topic's first message.
user-info-update-error = Error whiile fetching user info. Please try again later.

topic-ignored = This topic is marked as ignored; it is not related to any user.
