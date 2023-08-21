import asyncio
from datetime import datetime
from aiosmtpd.controller import Controller
from email import message_from_bytes
import re
import requests

regex = r'https://kingsumo\.com/giveaways/confirm/[a-zA-Z0-9]+/[a-zA-Z0-9]+'
total_pwnd = 0

async def call_url(url):
    r = requests.get(url)
    await time_print(r.status_code)
    if r.status_code == 200:
        global total_pwnd
        total_pwnd += 1
        await time_print("Total PWND: " + str(total_pwnd))

async def time_print(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def non_time_print(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

class MailHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # This part checks whether the mail coming in is actually
        # coming in to where it should, as in kianbrose.com which
        # is my domain. Technically not fully necessary but nice
        # to have.
        # if not address.endswith('@mail.kieranklukas.com'):
        #     print("Address does not end with @kieranklukas.com")
        #     return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'
    async def handle_DATA(self, server, session, envelope):
        # This one if the sender, so if it was sent to
        # someone@gmail.com mail_from will be that
        await time_print('Message from %s' % envelope.mail_from)

        # This is a string array of who it was sent to
        # like ['bob@xxxx.com','jeff@xxxx.com']
        # it can have a length of 1 if theres only 1 
        # person it was sent to
        await time_print('Message for %s' % envelope.rcpt_tos)

        # If you want to print EVERYTHING in the mail
        # including useless information, use this
        #print('Message data:\n')
        #for ln in envelope.content.decode('utf8', errors='replace').splitlines():
        #    print(f'> {ln}'.strip())


        # This code is to just read the text part of the email
        # in other words the useful part that we actually, as in
        # the actual text inside the mail
        plain_text_part = None
        email_message = message_from_bytes(envelope.content)
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                plain_text_part = part.get_payload(decode=True).decode('utf-8')
                break

        # This is to finish the mail and see that it finished
        # it can be removed, just visual

        if plain_text_part:
            # Do something with the plain text part
            await time_print("Plain text content:")
            print(plain_text_part)

            await time_print('End of message')

            urls = re.findall(regex, plain_text_part)

            for url in urls:
                await call_url(url)

        return '250 Message accepted for delivery'


# Here you start the actual server, hostname is your PRIVATE ipv4, and port has to be 25
# Change it to your actual local ipv4 or use localhost
controller = Controller(MailHandler(), hostname='192.168.10.88', port=25)
controller.start()
non_time_print("Running")
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    controller.stop()
    non_time_print("Stopped")
    exit()