import praw
import discord
from random import randint
from random import choice
import config

reddit = praw.Reddit( client_id= config.CLIENT_ID,
                      client_secret= config.CLIENT_SECRET ,
                      password= config.PASSWORD,
                      user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                      username= config.USERNAME,
                      check_for_async=False)

def check_image(urllink):
    ext = urllink[-4:]
    if ext == '.jpg' or ext == '.png':
        return True

    return False

def get_meme(sub,count):
    sub_reddit = reddit.subreddit(sub)
    hot_meme = sub_reddit.hot(limit=count)
    result =[]
    for submissions in hot_meme:
        temp = {"Title": submissions.title,
                  "Url": submissions.url,
                  "Upvotes": submissions.ups,
                  "Downvotes": submissions.downs,
                  "Redditurl": submissions.shortlink,
                  "Subreddit": sub
                  }
        result.append(temp)

    return result

def random_meme(num):
    if num == 0:
        subN = "memes"
    if num == 1:
        subN = "dankmemes"
    if num == 2:
        subN = "wholesomememes"
    if num == 3:
        subN = "aww"
    if num == 4:
        subN = "IndianDankMemes"

    r = get_meme(subN,100)
    requsted = choice(r)
    while not check_image(requsted["Url"]):
            requsted = choice(r)
        
    return{
        'Title':requsted["Title"],
        'Url': requsted["Url"],
        'Upvotes': requsted["Upvotes"],
        'Downvotes': requsted["Downvotes"],
        'Redditurl': requsted["Redditurl"],
        'Subreddit': requsted["Subreddit"]
    }


client = discord.Client()

@client.event
async def on_ready():

    print("I'm online!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith('$say'):
        text = msg.split('$say ',1)[1]
        await message.channel.send(text)
    
    if msg.lower().startswith("im"):
        text = msg.split("I'm ",1)[1]
        await message.channel.send(f"`hey {text}, I'm dad`")

    if msg.startswith('$help'):
        menu = "```1 $meme --> memes\n2 $wmeme --> wholesomememes\n3 $IDM --> IndianDankMemes\n4 $aww --> cute animals(sometimes human babies)\n5 $say --> text the message```"
        await message.channel.send(menu)

    if msg.startswith('$meme'):
        num = randint(0,1)
        meme = random_meme(num)
        text = meme['Title']
        img = meme['Url']
        sub = meme['Subreddit']
        await message.channel.send(f'```subreddit - r/{sub}\n{text}```')
        await message.channel.send(img)

    if msg.startswith('$IDM'):
        meme = random_meme(4)
        text = meme['Title']
        img = meme['Url']
        sub = meme['Subreddit']
        await message.channel.send(f'```subreddit - r/{sub}\n{text}```')
        await message.channel.send(img)

    if msg.startswith('$aww'):
        meme = random_meme(3)
        text = meme['Title']
        img = meme['Url']
        sub = meme['Subreddit']
        await message.channel.send(f'```subreddit - r/{sub}\n{text}```')
        await message.channel.send(img)

    if msg.startswith('$wmem'):
        meme = random_meme(2)
        text = meme['Title']
        img = meme['Url']
        sub = meme['Subreddit']
        await message.channel.send(f'```subreddit - r/{sub}\n{text}```')
        await message.channel.send(img)

    if msg.startswith('$MEME') or msg.startswith('$WMEME') or msg.startswith('$AWW'):
        await message.channel.send("why you shouting?")

client.run(config.TOKEN)