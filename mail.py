import asyncio
import imaplib
import time
from datetime import datetime

import aiohttp
import discord
import html2text
from discord import Webhook, AsyncWebhookAdapter


class EmailClass:
    def __init__(self):
        self.email = {
            'my@email.com': {
                'name': 'MyWebHookName',
                'pw': 'MyEmailPassword',
                'wh': 'MyWebHookUrl'
            }

        }

    def wait(self, sek: int):
        while True:
            self.send_mail()
            time.sleep(sek)
            print("Yeet")

    def send_mail(self):
        mail = imaplib.IMAP4_SSL('MyMailServer.eu', 993)
        i = 'my@emai.com'
        try:
            name = self.email[i]['name']
            print(name)
            password = self.email[i]['pw']
            url = self.email[i]['wh']
            mail.login(i, password)
            mail.select()
            mail.select(readonly=True)
            mail.select("inbox")

            result, data = mail.search(None, "ALL")
            ids = data[0]
            id_list = ids.split()
            for i in id_list:
                if 'seen' not in str(mail.fetch(i, 'FLAGS')).lower():
                    latest_email_id = i
                    result, data = mail.fetch(latest_email_id, "(RFC822)")
                    raw_email = data[0][1].decode('utf-8')
                    h = html2text.HTML2Text()
                    h.ignore_links = True
                    text = h.handle(raw_email)
                    end_string = text.split("|  |  |")[1]
                    embed = discord.Embed(title="Bewerbung",
                                          description=end_string)
                    embed.timestamp = datetime.utcnow()
                    asyncio.run(self.foo(embed, url, name))
            mail.store('1:*', '+FLAGS', '\\seen')
            print("Done")
            mail.close()
            mail.logout()
            time.sleep(10)
        except Exception as e:
            print(e)
            print("Failed")
            pass


    async def foo(self, embed, url, name):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url,
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=embed, username=name)


if __name__ == '__main__':
    EmailClass().wait(0)
