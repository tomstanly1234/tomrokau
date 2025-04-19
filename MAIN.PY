import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
GUILDID=discord.Object(id=1357757194011021402)#this is the one needed for server connection
intents=discord.Intents.default()
intents.message_content=True
client = commands.Bot(command_prefix="!",intents=intents)
activity_items = {'fish': ['Trout', 'Salmon', 'Prawn', 'Bass', 'Sardine', 'Dolphinfish', 'Sawfish'],'hunt': ['Rabbit', 'Deer', 'Boar', 'Wolf', 'Bear', 'Cougar', 'Phoenix'],'mine': ['Stone', 'Coal', 'Iron', 'Bauxite', 'Silver', 'Gold', 'Mythril']}
individualuserdatas={}
playerrecordwld={}
def update_stats(winner,loser= None,is_draw=False):
    c=[winner,loser]
    for player in c:
        if player and player.id not in playerrecordwld:
            playerrecordwld[player.id] = {'wins': 0, 'losses': 0, 'draws': 0}
    if is_draw:
        playerrecordwld[winner.id]['draws'] += 1
        playerrecordwld[loser.id]['draws'] += 1
    else:
        playerrecordwld[winner.id]['wins'] += 1
        playerrecordwld[loser.id]['losses'] += 1
@client.event
async def on_ready():
    print(f'The bot is ready as {client.user}!')
    try:
        synced=await client.tree.sync(guild=GUILDID)
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@client.tree.command(name='initialize', description='Initialize your account to bot', guild=GUILDID)
async def initialize(interaction):
    user_id=interaction.user.id
    if user_id not in individualuserdatas:
        individualuserdatas[user_id]={
            'coins': 5000,
            'items': {item: 0 for item in ['Trout', 'Salmon', 'Prawn', 'Bass', 'Sardine', 'Dolphinfish', 'Sawfish','Rabbit', 'Deer', 'Boar', 'Wolf', 'Bear', 'Cougar', 'Phoenix','Stone', 'Coal', 'Iron', 'Bauxite', 'Silver', 'Gold', 'Mythril'
            ]},
            'gear': {'Rod': 1, 'Gun': 1, 'Pickaxe': 1}
        }
        await interaction.response.send_message(f"Welcome, {interaction.user.display_name}! You're now registered with 5000 coins and basic gear.")
    else:
        await interaction.response.send_message("You're already registered. Try out our features")

def doactivities(user_id, category,gear_level):
    items = activity_items.get(category, [])
    if not items:
        return []
    weights=[50,25,15,40,30,7,4]
    result=random.choices(items,weights=weights,k=random.randint(1,gear_level))
    for item in result:
        individualuserdatas[user_id]['items'][item]+=1
    return result

async def activityshower(interaction,category:str):
    await interaction.response.defer()
    userid=interaction.user.id
    if userid not in individualuserdatas:
        return await interaction.followup.send("Please initialize first using '/initialize'.")
    gear_mapping={'fish':'Rod','hunt':'Gun','mine':'Pickaxe'}
    gear=individualuserdatas[userid]['gear'][gear_mapping[category]]
    result=doactivities(userid,category,gear)
    if not result:
        return await interaction.followup.send(f"You {category}ed nothing. Try harder next time!")

    summary = ', '.join(result)
    if category==mine:
        await interaction.followup.send(f"You {category}d: {summary}!")
    else:
        await interaction.followup.send(f"You {category}ed: {summary}!")
    k=set(result)
    for item in k:
        if item=="Rabbit":
            em=discord.Embed(title="You Caught a Rabbit", description="Quite a common catch!",color=discord.Color.gold())
            em.add_field(name="You can sell it in the market", value="Price: 20 coins", inline=False)
            em.set_thumbnail(url="https://media.istockphoto.com/id/1311272463/photo/wild-rabbit.jpg?s=612x612&w=0&k=20&c=p-90jo8libyLj5Oy4HhwXtb5D5MDiTUT3B4Aa4yBJFE=")
            await interaction.followup.send(embed=em)
        elif item=="Deer":
            em=discord.Embed(title="You Caught a Deer", description="Great Catch", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 40 coins", inline=False)
            em.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuMm_6hpzc1mo7eqOKIzB0Q75cJ6Zyv2XT5Q&s")
            await interaction.followup.send(embed=em)
        elif item=="Boar":
            em=discord.Embed(title="You Caught a Boar", description="Great Catch!!", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 300 coins", inline=False)
            em.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgOiBrvO7SyOztnGjCWlb1ndL4V8y5g5wI5A&s")
            await interaction.followup.send(embed=em)
        elif item=="Wolf":
            em=discord.Embed(title="You Caught a wolf", description="INSANE Catch!!", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 500 coins", inline=False)
            em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Eurasian_wolf_2.jpg/1200px-Eurasian_wolf_2.jpg")
            await interaction.followup.send(embed=em)
        elif item=="Cougar":
            em=discord.Embed(title="You Caught a COUGAR", description="IMPRESSIVE Catch!!",color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 700 coins", inline=False)
            em.set_thumbnail(url="https://media.hswstatic.com/eyJidWNrZXQiOiJjb250ZW50Lmhzd3N0YXRpYy5jb20iLCJrZXkiOiJnaWZcL2NvdWdhci0xLmpwZyIsImVkaXRzIjp7InJlc2l6ZSI6eyJ3aWR0aCI6ODI4fX19")
            await interaction.followup.send(embed=em)
        elif item=="Phoenix":
            em=discord.Embed(title="YOU CAUGHT A MYTHICAL PHOENIX", description="IMPOSSIBLE Catch!!",color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 7000 coins", inline=False)
            em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Phoenix-Fabelwesen.jpg/250px-Phoenix-Fabelwesen.jpg")
            await interaction.followup.send(embed=em)
        elif item=="Bear":
            em=discord.Embed(title="You Caught a bear", description="RARE Catch!!", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 600 coins", inline=False)
            em.set_thumbnail(url="https://cdn.britannica.com/17/235817-050-97A76099/American-black-bear-ursus-americanus-standing-stream-British-Columbia-Canada.jpg")
            await interaction.followup.send(embed=em)
        elif item=="Sawfish":
            em = discord.Embed(title="You Caught a SAWFISH",description="mythical Catch!!", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 5000 coins", inline=False)
            em.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Sawfish_Pristis_zijsron_Genova_Aquarium.jpg/1200px-Sawfish_Pristis_zijsron_Genova_Aquarium.jpg")
            await interaction.followup.send(embed=em)
        elif item=="Dolphinfish":
            em = discord.Embed(title="You Caught a Dolphinfish",description="a very rare Catch in this subcontinent youre a master!!!",color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 1500 coins", inline=False)
            em.set_thumbnail(url="https://www.montereybayaquarium.org/globalassets/mba/images/animals/fishes/dolphinfish-tr19-0262.jpg")
            await interaction.followup.send(embed=em)
        elif item=="Sardine":
            em = discord.Embed(title="You Caught some tonnes of sardines!!!!!!", description="HEY KEEP FISHING THOSE!!",color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 500 coins", inline=False)
            em.set_thumbnail(
                url="https://cdn.britannica.com/75/143775-050-020FF82D/Pilchard-European-sardine.jpg?w=400&h=225&c=crop")
            await interaction.followup.send(embed=em)
        elif item=="Bass":
            em = discord.Embed(title="You Caught a HUGE school of BASS", description="Insane Catch!!",
                               color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 250 coins", inline=False)
            em.set_thumbnail(
                url="https://images.ctfassets.net/pujs1b1v0165/2AvtJ9pcEJ4bjxkR8Vc5bJ/5d1033f3c8f450f73cf54b521bb06b4e/How_to_Find_the_Right_Depth_for_Bass.jpg?fit=fill&w=1200&h=630")
            await interaction.followup.send(embed=em)
        elif item=="Prawn":
            em=discord.Embed(title="You Caught some prawns", description="COOL Catch!!", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 100 coins", inline=False)
            em.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrCqgcRxrdKos5cT5wPciYLXM5pql16N0b1A&s")
            await interaction.followup.send(embed=em)
        elif item=="Salmon":
            em = discord.Embed(title="You Caught a school of Salmon!",description="good Catch!! keep fishing",color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 45 coins", inline=False)
            em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/3/39/Salmo_salar.jpg")
            await interaction.followup.send(embed=em)
        elif item=="Trout":
            em = discord.Embed(title="You Caught a trout",description="common Catch!! keep fishing",color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 10 coins", inline=False)
            em.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjqP5V-iEWMf8MPEsEJQ9h8g-LgVcae_egyw&s")
            await interaction.followup.send(embed=em)
        elif item=="Bauxite":
            em = discord.Embed(title="You mined bauxite", description="keep digging you may find more !!",
                               color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 105 coins", inline=False)
            em.set_thumbnail(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScBbaJbO-rfvKNZxGg2dD-lnaXqCITe7a6Ig&s")
            await interaction.followup.send(embed=em)
        elif item =="Silver":
            em = discord.Embed(title="You mined SILVER", description="great mine!!", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 205 coins", inline=False)
            em.set_thumbnail(
                url="https://media.gettyimages.com/id/157526585/photo/small-pieces-of-strong-metal-ore.jpg?s=612x612&w=gi&k=20&c=BNAeWRPS76jhaeJ_giv11T7eKcHUKk4rfDXNV195gQs=")
            await interaction.followup.send(embed=em)
        elif item =="Coal":
            em = discord.Embed(title="You mined Coal", description="Great Mine!!", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 20 coins", inline=False)
            em.set_thumbnail(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRFW3i6R6qZYhTJ_HmI259GxpaxM4bRNKQckg&s")
            await interaction.followup.send(embed=em)
        elif item =="Mythril":
            em = discord.Embed(title="You have mined the impossible!!!!!!", description="WHAT A STROKE OF LUCK!!",
                               color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 30000 coins", inline=False)
            em.set_thumbnail(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1_C04M_NjRxHZfnWCdqbe1KDTfJMHk6tmkg&s")
            await interaction.followup.send(embed=em)
        elif item =="Gold":
            em = discord.Embed(title="You mined GOLD ORE!!", description="RARE MINE!!", color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 1000 coins", inline=False)
            em.set_thumbnail(
                url="https://png.pngtree.com/png-clipart/20240319/original/pngtree-pure-gold-ore-isolated-png-image_14630217.png")
            await interaction.followup.send(embed=em)
        elif item =="Stone":
            em = discord.Embed(title="You mined a stone", description="Try better next time!!",
                               color=discord.Color.gold())
            em.add_field(name="You Can Sell in Market", value="Price: 2 coins", inline=False)
            em.set_thumbnail(url="https://img.freepik.com/free-psd/grey-boulder-rock-isolated-transparent-background_632498-25568.jpg")
            await interaction.followup.send(embed=em)
@client.tree.command(name='fish', description='Go fishing!', guild=GUILDID)
async def fish(interaction: discord.Interaction):
    await activityshower(interaction, 'fish')

@client.tree.command(name='hunt', description='Go hunting!', guild=GUILDID)
async def hunt(interaction: discord.Interaction):
    await activityshower(interaction, 'hunt')

@client.tree.command(name='mine', description='Go mining!', guild=GUILDID)
async def mine(interaction: discord.Interaction):
    await activityshower(interaction, 'mine')
class MarketSellButton(discord.ui.Button):
    def __init__(self, userid: int, item_name: str):
        self.userid=userid
        self.item = item_name
        super().__init__(label=f"Sell {item_name}", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id!=self.userid:
            return await interaction.response.send_message("This isn't your session. Your responses arent tracked",ephemeral=True)
        qty=individualuserdatas[self.userid]['items'].get(self.item,0)
        if qty<1:
            return await interaction.response.send_message(f"You have no {self.item} to sell.",ephemeral=True)
        itemprices = {'Trout': 10, 'Salmon':45,'Prawn':100,'Bass': 250,'Sardine':500,'Dolphinfish': 1500, 'Sawfish': 5000, 'Rabbit': 20, 'Deer': 40,'Boar': 300, 'Wolf': 500, 'Bear': 600, 'Cougar': 700, 'Phoenix': 7000,'Stone': 2, 'Coal': 20, 'Iron': 30, 'Bauxite': 105, 'Silver': 205,'Gold': 1000, 'Mythril': 30000}
        total=itemprices.get(self.item, 1)*qty
        individualuserdatas[self.userid]['coins']+=total
        individualuserdatas[self.userid]['items'][self.item]=0
        await interaction.response.send_message(f"Sold {qty} {self.item} for {total} coins!")


class MarketView(discord.ui.View):
    def __init__(self, userid: int):
        super().__init__()
        self.userid=userid
        for item,qty in individualuserdatas[userid]['items'].items():
            if qty>0:
                self.add_item(MarketSellButton(userid, item))
        self.add_item(discord.ui.Button(label="Exit",style=discord.ButtonStyle.red,custom_id="exit"))
        @discord.ui.button(label="Exit", style=discord.ButtonStyle.red, row=4)
        async def exit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.userid:
                return await interaction.response.send_message("This isn't your menu!", ephemeral=True)
            await interaction.response.edit_message(content="Market closed.", view=None)
            self.stop()

@client.tree.command(name='market', description='Sell your items', guild=GUILDID)
async def market(interaction):
    userid=interaction.user.id
    if userid not in individualuserdatas:
        return await interaction.response.send_message("Please initialize first.",ephemeral=True)
    if not any(individualuserdatas[userid]['items'].values()):
        return await interaction.response.send_message("You have nothing to sell!",ephemeral=True)
    await interaction.response.send_message("Select items to sell:", view=MarketView(userid),ephemeral=True)

@client.tree.command(name='coinflip', description='Flip a coin and bet on the outcome(in the choice part put heads or tails)', guild=GUILDID)
async def coinflip(interaction: discord.Interaction, choice: str, bet: int):
    user_id=interaction.user.id
    if user_id not in individualuserdatas:
        return await interaction.response.send_message("Please initialize first.", ephemeral=True)
    if bet<=0:
        return await interaction.response.send_message("Bet must be non zero and positive.➕", ephemeral=True)
    if individualuserdatas[user_id]['coins'] < bet:
        return await interaction.response.send_message("you Too broke for that kinda bet😔. maybe put some less money .", ephemeral=True)
    choice=choice.lower()
    if choice not in ['heads','tails']:
        return await interaction.response.send_message("Choose 'heads' or 'tails'.", ephemeral=True)
    await interaction.response.defer()
    await asyncio.sleep(1)
    result = random.choice(['heads', 'tails'])
    if result == choice:
        individualuserdatas[user_id]['coins']+=bet
        await interaction.followup.send(f"🎉 🎉 🎉  {result.capitalize()}! You won {bet} coins!")
    else:
        individualuserdatas[user_id]['coins']-=bet
        await interaction.followup.send(f"💀🥀 {result.capitalize()}! You lost {bet} coins.💀🥀")

class RPSView(discord.ui.View):
    def __init__(self, user_id: int, bet: int):
        super().__init__(timeout=30)
        self.user_id=user_id
        self.bet=bet
    @discord.ui.button(label="🪨Rock🪨",style=discord.ButtonStyle.blurple)
    async def rock(self, interaction: discord.Interaction, button:discord.ui.Button):
        await self.play_game(interaction,'rock')
    @discord.ui.button(label="📄Paper📄", style=discord.ButtonStyle.green)
    async def paper(self, interaction: discord.Interaction, button:discord.ui.Button):
        await self.play_game(interaction,'paper')
    @discord.ui.button(label="✂️Scissors️✂️", style=discord.ButtonStyle.red)
    async def scissors(self, interaction: discord.Interaction, button:discord.ui.Button):
        await self.play_game(interaction,'scissors')
    async def play_game(self, interaction: discord.Interaction, player_choice: str):
        if interaction.user.id !=self.user_id:
            return await interaction.response.send_message("This isn't your game!", ephemeral=True)
        bot_choice =random.choice(['rock','paper','scissors'])
        result=None
        outcome=0
        if player_choice==bot_choice:
            result="It's a tie!"
        elif (player_choice=='rock' and bot_choice=='scissors') or \
                (player_choice=='paper' and bot_choice =='rock') or \
                (player_choice=='scissors' and bot_choice =='paper'):
            result=f"You win! {player_choice} beats {bot_choice}."
            outcome=1
        else:
            result=f"You lose! {bot_choice} beats {player_choice}."
            outcome=-1
        if outcome==1:
            individualuserdatas[self.user_id]['coins']+=self.bet
            color=discord.Color.green()
        elif outcome ==-1:
            individualuserdatas[self.user_id]['coins']-=self.bet
            color=discord.Color.red()
        elif outcome==0:
            color=discord.Color.gold()
        em=discord.Embed(title="Rock🪨 Paper📄 Scissors✂️",description=result,color=color)
        em.add_field(name="Your Choice",value=player_choice.capitalize(),inline=True)
        em.add_field(name="Bot's Choice",value=bot_choice.capitalize(),inline=True)
        em.add_field(name="Bet",value=f"{self.bet} coins",inline=False)
        em.add_field(name="New Balance",value=f"{individualuserdatas[self.user_id]['coins']} coins",inline=False)
        for child in self.children:
            child.disabled=True
        await interaction.response.edit_message(embed=em,view=self)
        self.stop()
@client.tree.command(name='rps', description='Play Rock Paper Scissors', guild=GUILDID)
async def rps(interaction: discord.Interaction, bet: int):
    user_id=interaction.user.id
    if user_id not in individualuserdatas:
        return await interaction.response.send_message("Please initialize first.", ephemeral=True)
    if bet<=0:
        return await interaction.response.send_message("Bet must be positive.", ephemeral=True)
    if individualuserdatas[user_id]['coins'] < bet:
        return await interaction.response.send_message("Not enough coins.", ephemeral=True)
    view = RPSView(user_id, bet)
    em = discord.Embed(title="Rock Paper Scissors", description=f"Bet: {bet} coins\nChoose your move!",color=discord.Color.blue())
    await interaction.response.send_message(embed=em, view=view)
class GuessModal(discord.ui.Modal, title='Guess the Number'):
    guess = discord.ui.TextInput(label='Enter your guess (1-100)')
    def __init__(self, target: int, bet: int, userid: int):
        super().__init__()
        self.target=target
        self.bet=bet
        self.userid=userid
    async def on_submit(self,interaction:discord.Interaction):
        try:
            player_guess=int(self.guess.value)
            if player_guess>100 or player_guess<1:
                return await interaction.response.send_message("Please enter a number between 1-100!", ephemeral=True)
            difference = abs(self.target-player_guess)
            if player_guess==self.target:
                win_amount=self.bet * 5
                individualuserdatas[self.userid]['coins']+=win_amount
                await interaction.response.send_message(
                    f"🎉🎉🎉🎉 JACKPOT! You guessed it exactly! You win {win_amount} coins!")
            elif difference<=5:
                win_amount=self.bet * 2
                individualuserdatas[self.userid]['coins']+=win_amount
                await interaction.response.send_message(
                    f"🔥🎉🎉🔥 Close! The number was {self.target}. You win {win_amount} coins!")
            elif difference <= 15:
                individualuserdatas[self.userid]['coins'] += self.bet
                await interaction.response.send_message(
                    f"👍 Not bad! The number was {self.target}. You get your {self.bet} coins back.")
            else:
                individualuserdatas[self.userid]['coins'] -= self.bet
                await interaction.response.send_message(
                    f"🤡🤡Oof! The number was {self.target}.WAY OFF! You lose {self.bet} coins...")
        except ValueError:
            await interaction.response.send_message("Please enter a valid number so that we can proceed with the game!🤡🤡", ephemeral=True)

@client.tree.command(name='guess', description='Guess a number between 1-100',guild=GUILDID)
async def guess(interaction: discord.Interaction, bet: int):
    user_id=interaction.user.id
    if user_id not in individualuserdatas:
        return await interaction.response.send_message("Please initialize first.",ephemeral=True)
    if bet<=0:
        return await interaction.response.send_message("Bet must be positive and non zero.",ephemeral=True)
    if individualuserdatas[user_id]['coins']<bet:
        return await interaction.response.send_message("🥀🥀🥀Not enough coins.",ephemeral=True)
    target=random.randint(1,100)
    modal=GuessModal(target,bet,user_id)
    await interaction.response.send_modal(modal)
class BlackjackView(discord.ui.View):
    def __init__(self,user_id:int,bet:int):
        super().__init__(timeout=60)
        self.user_id=user_id
        self.bet=bet
        self.deck = self.create_deck()
        self.player_hand=[]
        self.dealer_hand=[]
        self.game_over=False
        self.player_hand.append(self.draw_card())
        self.dealer_hand.append(self.draw_card())
        self.player_hand.append(self.draw_card())
        self.dealer_hand.append(self.draw_card())
    def create_deck(self):
        suits=['Hearts','Diamonds','Clubs','Spades']
        values=['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        deck=[]
        for suit in suits:
            for value in values:
                card=f"{value}of {suit}"
                deck.append(card)
    def draw_card(self):
        return self.deck.pop()
    def calculate_hand(self, hand):
        value=0
        aces=0
        for card in hand:
            card_value=card.split()[0]
            if card_value in ['J','Q','K']:
                value+=10
            elif card_value=='A':
                value+=11
                aces+=1
            else:
                value+=int(card_value)

        while value>21 and aces:
            value-=10
            aces-=1

        return value

    async def update_message(self, interaction: discord.Interaction):
        player_value = self.calculate_hand(self.player_hand)
        dealer_value = self.calculate_hand(self.dealer_hand)
        if self.game_over:
            dealer_cards = "\n".join(self.dealer_hand)
            result = ""

            if player_value > 21:
                result = "You busted! You lose!"
                outcome = -1
            elif dealer_value > 21:
                result = "Dealer busted! You win!"
                outcome = 1
            elif player_value > dealer_value:
                result = "You win!"
                outcome = 1
            elif player_value < dealer_value:
                result = "You lose!"
                outcome=-1
            else:
                result = "It's a tie!"
                outcome=0

            if outcome==1:
                individualuserdatas[self.user_id]['coins']+=self.bet
                color = discord.Color.green()
            elif outcome==-1:
                individualuserdatas[self.user_id]['coins']-=self.bet
                color=discord.Color.red()
            else:
                color=discord.Color.gold()
            em=discord.Embed(title="Blackjack", color=color)
            em.add_field(name="Your Hand", value="\n".join(self.player_hand) + f"\nTotal: {player_value}", inline=False)
            em.add_field(name="Dealer's Hand", value=dealer_cards + f"\nTotal: {dealer_value}", inline=False)
            em.add_field(name="Result",
                         value=f"{result}\n\nNew Balance: {individualuserdatas[self.user_id]['coins']} coins",
                         inline=False)
            await interaction.response.edit_message(embed=em, view=None)
            self.stop()
        else:
            em=discord.Embed(title="Blackjack", color=discord.Color.blue())
            em.add_field(name="Your Hand", value="\n".join(self.player_hand) + f"\nTotal: {player_value}", inline=False)
            em.add_field(name="Dealer's Hand", value=f"{self.dealer_hand[0]}\nand 1 hidden card", inline=False)
            em.add_field(name="Bet", value=f"{self.bet} coins", inline=False)

            await interaction.response.edit_message(embed=em, view=self)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("This isn't your game!", ephemeral=True)

        self.player_hand.append(self.draw_card())
        player_value = self.calculate_hand(self.player_hand)

        if player_value > 21:
            self.game_over = True

        await self.update_message(interaction)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("This isn't your game!", ephemeral=True)
        self.game_over = True
        player_value = self.calculate_hand(self.player_hand)

        while self.calculate_hand(self.dealer_hand) < 17 and player_value <= 21:
            self.dealer_hand.append(self.draw_card())

        await self.update_message(interaction)


@client.tree.command(name='blackjack', description='Play Blackjack (21)',guild=GUILDID)
async def blackjack(interaction: discord.Interaction,bet:int):
    user_id = interaction.user.id
    if user_id not in individualuserdatas:
        return await interaction.response.send_message("Please initialize first.", ephemeral=True)

    if bet<=0:
        return await interaction.response.send_message("Bet must be positive.💵💵💵", ephemeral=True)

    if individualuserdatas[user_id]['coins'] < bet:
        return await interaction.response.send_message("Not enough coins.", ephemeral=True)

    view = BlackjackView(user_id, bet)
    await interaction.response.send_message("Starting Blackjack...💪🏼💪🏼💪🏼", view=view)
    await view.update_message(interaction)

class ChallengeView(discord.ui.View):
    def __init__(self, challenger, opponent, bet):
        super().__init__(timeout=30)
        self.challenger=challenger
        self.opponent=opponent
        self.bet=bet
        self.value=None

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction,button: discord.ui.Button):
        if interaction.user!=self.opponent:
            await interaction.response.send_message("NOT FOR YOU.", ephemeral=True)
            return
        self.value=True
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction,button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("NOT FOR YOU.", ephemeral=True)
            return
        self.value=False
        self.stop()
        await interaction.response.defer()
class TicTacToeButton(discord.ui.Button):
    def __init__(self,x,y):
        super().__init__(style=discord.ButtonStyle.secondary, label=' ',row=y)
        self.x=x
        self.y=y
    async def callback(self, interaction: discord.Interaction):
        view: TicTacToe=self.view
        if view.current_player!=interaction.user:
            return await interaction.response.send_message("Not your turn.", ephemeral=True)
        if view.board[self.y][self.x]!=0:
            return await interaction.response.send_message("Spot already taken.", ephemeral=True)
        if view.current_player == view.player1:
            mark=1
        else:
            mark=2
        if mark==1:
            self.label='❌'
        else:
            self.label='⭕'
        if mark==1:
            self.style=discord.ButtonStyle.red
        else:
            self.style=discord.ButtonStyle.blurple
        view.board[self.y][self.x]=mark
        winner=view.check_winner()
        if winner:
            for child in view.children:
                child.disabled=True
            if winner==1:
                update_stats(view.player1, view.player2)
                content=f"{view.player1.mention} wins!"
                winner_user=view.player1
            elif winner==2:
                update_stats(view.player2, view.player1)
                content=f"{view.player2.mention} wins!"
                winner_user=view.player2
            else:
                update_stats(view.player1, view.player2, is_draw=True)
                content="It's a tie!"
                winner_user=None
            if winner_user and view.bet > 0:
                winner_id=str(winner_user.id)
                individualuserdatas[winner_id]['coins']+=view.bet*2
                content+=f"\n🏆 {view.bet*2} coins awarded!"
            await interaction.response.edit_message(content=content,view=view)
            view.stop()
            return
        if view.current_player==view.player1:
            view.current_player=view.player2
        else:
            view.current_player=view.player1
        await interaction.response.edit_message(content=f"{view.current_player.mention}'s turn",view=view)


class TicTacToe(discord.ui.View):
    def __init__(self, player1, player2, bet):
        super().__init__()
        self.player1=player1
        self.player2=player2
        self.current_player=player1
        self.board=[[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.bet=bet
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x,y))
    def check_winner(self):
        b=self.board
        for i in range(3):
            if b[i][0]==b[i][1]==b[i][2]!=0:
                return b[i][0]
        for i in range(3):
            if b[0][i]==b[1][i]==b[2][i]!=0:
                return b[0][i]
        if b[0][0]==b[1][1]==b[2][2]!=0:
            return b[0][0]
        if b[0][2] ==b[1][1]==b[2][0]!=0:
            return b[0][2]
        if all(b[y][x] !=0 for x in range(3) for y in range(3)):
            return 3
        return None

@client.tree.command(name='tictactoe',description='Play Tic Tac Toe with betting!',guild=GUILDID)
async def tictactoe(interaction: discord.Interaction, opponent: discord.Member, bet: int):
    if opponent.bot or opponent==interaction.user:
        return await interaction.response.send_message("Invalid opponent. The user might be a bot or you are inviting yourself!",ephemeral=True)
    if bet<=0:
        return await interaction.response.send_message("Bet must be more than 0.💵",ephemeral=True)
    player1_id=str(interaction.user.id)
    player2_id=str(opponent.id)
    if player1_id not in individualuserdatas or player2_id not in individualuserdatas:
        return await interaction.response.send_message("😄players must be registered.😄",ephemeral=True)
    if individualuserdatas[player1_id]['coins'] < bet or individualuserdatas[player2_id]['coins'] < bet:
        return await interaction.response.send_message("⛔️⛔️Betting is too high for one of the parties!⛔️⛔️",ephemeral=True)
    view=ChallengeView(interaction.user,opponent,bet)
    await interaction.response.send_message(f"{opponent.mention},do you accept the Tic Tac Toe challenge for {bet} 💵money⁉️",view=view)
    timeout=await view.wait()
    if view.value is None:
        return await interaction.followup.send("TIME LIMIT EXCEEDED. No response.😞",ephemeral=True)
    elif view.value is False:
        return await interaction.followup.send("Challenge declined. User does not want to play with you!😞😞",ephemeral=True)
    individualuserdatas[player1_id]['coins']-=bet
    individualuserdatas[player2_id]['coins']-=bet
    game_view=TicTacToe(interaction.user, opponent, bet)
    await interaction.followup.send(f"{interaction.user.mention} vs {opponent.mention}\n{interaction.user.mention}'s turn (Player 1)\n**Bet: {bet} coins each!",view=game_view)
@client.tree.command(name='yourstats', description='know your stats', guild=GUILDID)
async def stats(interaction: discord.Interaction):
    userid=interaction.user.id
    stuff=individualuserdatas[userid]
    for userid1,data in individualuserdatas.items():
        if userid1==userid:
            await interaction.response.send_message(f"You Have {data['coins']}")
            await interaction.followup.send(f" {data['items']} ")
@client.tree.command(name='richest',description='Know your richest member',guild=GUILDID)
async def rich(interaction: discord.Interaction):
    maxi=-1
    richuser=None
    for userid, data in individualuserdatas.items():
        if data['coins']>maxi:
            maxi=data['coins']
            richuser=userid
    if richuser:
        await interaction.response.send_message(f"🤑🤑🤑🤑🤑🤑🤑🤑🤑🤑The richest user is <@{richuser}> with {maxi} coins!🤑🤑🤑🤑🤑🤑🤑🤑🤑")
    else:
        await interaction.response.send_message("ERROR generating.")



client.run('')
