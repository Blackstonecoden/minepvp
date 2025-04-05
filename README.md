## 📌 Information
This is an open-source discord app for the MinePvP Discord. 
Key features:
- welcome-role
- welcome messages
- logs
- temp-channels
- tickets
- bug-reports

## 🔌 Requirements
- [Python](https://www.python.org/)
- [MariDB](https://mariadb.org/) or [MySQL](https://www.mysql.com/)

## 🔧 Installation
Download the [code](https://github.com/Blackstonecoden/minepvp/archive/refs/heads/main.zip) from this repository. Setup the `.env` file in the root direcotry and fill it with your cridentials.
<details open>
  <summary style="font-size: 18px; cursor: pointer;">
    .env
  </summary>

```env
TOKEN = 123456
```
</details>

Create the `config.json`. Here is the reference.
<details open>
  <summary style="font-size: 18px; cursor: pointer;">
    config.json
  </summary>

```json
{
    "join_role": 1234,

    "categories": {
        "tickets": 1234,
        "temp_channels": 1234
    },
    
    "channels": {
        "chat": 1234,

        "temp_join": 1234,
        "ticket_support": 1234,
        "bug_reports": 1234,
        "bug_forum": 1234,

        "messages_log": 1234,
        "join_leave_log": 1234,
        "punishments_log": 1234

    },

    "ticket_types": {
        "general": {
            "disabled": false,
            "roles": [1234 ,1234],
            "name": "General Support",
            "description": "Need help or have a question?",
            "short_name": "General",
            "emoji": "📨",
            "discord_emoji": "mail"
        },
        "report_user": {
            "disabled": false,
            "roles": [1234, 1234],
            "name": "Report User",
            "description": "Report a user who violates our rules",
            "short_name": "Report",
            "emoji": "🚫",
            "discord_emoji": "block"
        },
        "appeal": {
            "disabled": false,
            "roles": [1234, 1234],
            "name": "Appeal",
            "description": "Submit an appeal for a punishment or ban",
            "short_name": "Appeal",
            "emoji": "📄",
            "discord_emoji": "file_text"
        },
        "billing": {
            "disabled": false,
            "roles": [1234, 1234],
            "name": "Billing Support",
            "description": "Assistance with billing issues",
            "short_name": "Billing",
            "emoji": "💲",
            "discord_emoji": "dollar"
        }
    },

    "bug_forum_tags": {
        "pending": {
            "tag_id": 1234
        },
        "discord": {
            "tag_id": 1234
        },
        "bot": {
            "tag_id": 1234
        },
        "lifesteal": {
            "tag_id": 1234
        },
        "boxpvp": {
            "tag_id": 1234
        }
    },

    "emojis": {
        "book":                 "<:name:id>",
        "box":                  "",
        "mail":                 "",
        "block":                "",
        "user_plus":            "",
        "user_minus":           "",
        "file_text":            "",
        "dollar":               "",
        "trash":                "",
        "alert_triangle":       "",
        "message_circle":       "",
        "play_circle":          "",
        "users":                "",
        "clock":                "",

        "check_green":          "",

        "x_red":                "",
        "trash_red":            ""
    }
}
```
</details>

Create a folder called `data` and create two files called `bug_reports.json` and `ticket_list.json`. Fill both with `{}`.

Download [GG Sans](https://font.download/font/gg-sans-2) and create a folder called `fonts`. Put the `gg sans Bold.ttf` to `ggsans.ttf` and place it in the folder.