#wersja: któraś_tam_nie_pamiętam.0

import discord #to musi być bo sobie zrobi krzywde bez tego
import base64 #to też musi być bo czymś musi kodować
import zlib #a to tak dodatkowo jakby komuś za mało było



def loading_animation(progress): #to jest bardzo sigma animacja progress bara
    progress = min(progress, 100)
    bar = '█' * (progress // 2) + '_' * (50 - (progress // 2))
    print(f'\r|{bar}| {progress}%', end='', flush=True)



async def fetch_messages(channel): #to jest syzyf co bierze wiadmości z serwera
    messages = []
    async for msg in channel.history(limit=None, oldest_first=True):
        messages.append(msg)
        if len(messages) % 50 == 0: #to jest po to żeby się animacja robiła jak się przesyła
            loading_animation(int(len(messages) / 0.5))
    loading_animation(100)
    return messages



async def send_message(channel, message): #no ciekawe co "wyślij wiadmość" robi, chyba wysyła wiadmość
    await channel.send(message) #tylko że na kanał konkretny



async def history(channel_name): #to mi fetchuje z konkretnego kanału
    channel = discord.utils.get(client.get_all_channels(), name=channel_name)
    if channel:
        messages = await fetch_messages(channel)
        return "".join(msg.content for msg in messages)
    return None



async def post(channel_name, message): #a to tludne bylo
    channel = discord.utils.get(client.get_all_channels(), name=channel_name)
    if channel:
        if len(message) <= 2000: #to jest po to bo discord ma wylew i jak jest >2000 to nie wyślesz wiadmośći
            await send_message(channel, message)
        else: #no więc jak nie moge to przez noge
            parts = [message[i:i+2000] for i in range(0, len(message), 2000)] #dzieli mi na kawałki po 2000 ale przez to że to base85 to nie działa dokładnie
            total_parts = len(parts)
            for idx, part in enumerate(parts, 1):
                await send_message(channel, part)
                loading_animation(int((idx / total_parts) * 100)) # ma być ładnie ma być ładnie ma być ładnie ma być ładnie
        loading_animation(100)
        print("\nFile uploaded successfully.")
    else:
        print(f"Channel {channel_name} not found.")



async def create_channel(channel_name, category_name="files"): #ciekawe co ten cąły "tworzenie kanału" robi
    guild = client.guilds[0] #to to jes takie co discord musi bo sie udusi inaczej, bo on musi wiedzieć że ja jestem dobrym człowiekiem czy coś
    category = discord.utils.get(guild.categories, name=category_name) or await guild.create_category(name=category_name)
    if not discord.utils.get(category.channels, name=channel_name):
        await guild.create_text_channel(name=channel_name, category=category)



def file_to_base64(file_path): #no to tu mieli i mieli i mieli i daje mi z pliku text
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
            compressed_data = zlib.compress(data, level=9) #to jest kompresowanie na max poziomie co zlib daje
            return base64.b85encode(compressed_data).decode('utf-8') #a to mi na base85 zamienia
    except FileNotFoundError: #to takie śmieszne jak się nie uda
        return None
    except Exception as e:
        return f"Error: {e}"



def base64_to_file(base64_string, output_file_path): #a to odmiela
    try:
        decoded_data = base64.b85decode(base64_string.encode('utf-8')) #bierze ten tekst odmiela
        decompressed_data = zlib.decompress(decoded_data) #i tą kompresje też
        with open(output_file_path, 'wb') as output_file: #i se pliczek robi znowu
            output_file.write(decompressed_data)
        return "File successfully created."
    except Exception as e: #a to jakby sie zabiło coś
        return f"Error: {e}"



def read_token_from_file(): #a to tylko po to żeby dostępu publicznie do tokenu bota nie dawać, bo mnie discord zabije czy coś
    try:
        with open('token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Token file not found.")
        return None



intents = discord.Intents.default() #o to jest discordowe, musi być bo nie zadziała, do dosłownie defiuje client bota więc no
intents.presences = False
intents.members = True
client = discord.Client(intents=intents) #ja tam bym to wywalił ale musi być



@client.event #tu to sie dużo za dużo dzieje
async def on_ready():
    while True:
        user_input = input("/download, /upload, or /files: ") #wybierasz sobie
        command, *args = user_input.split(' ') #z tego bierze jakby typ komendy i jej treść
        if command == "/download" and args: #tu znowu mieli
            file_name = args[0]
            channel_name = bytes(file_name, 'utf-8').hex()
            print(f"Downloading [{file_name}] from channel [{channel_name}]:")
            base64_message = await history(channel_name)
            if base64_message:
                result = base64_to_file(base64_message, file_name)
                print(f"\n{result}")
            else:
                print("There is no such file.")
        elif command == "/upload" and args: #a tu jak chcesz inne, to mieli inaczej
            file_path = args[0]
            file_name = file_path.split('/')[-1]
            channel_name = bytes(file_name, 'utf-8').hex()
            print(f"Uploading file [{file_name}] to channel [{channel_name}]:")
            base64_message = file_to_base64(file_path)
            if base64_message:
                await create_channel(channel_name)
                await post(channel_name, base64_message)
            else:
                print("Error uploading file.")
        elif command == "/files": #a to proste bardzo bo tam są dziwne nazwy na tym discordzie tych plików
            guild = client.guilds[0]
            category = discord.utils.get(guild.categories, name="files")
            if category:
                print("Your files:")
                for channel in category.channels:
                    channel_name = bytes.fromhex(channel.name).decode('utf-8') #to tu robi że można sobie normalnie zobaczyć
                    print(channel_name)



TOKEN = read_token_from_file() #a to to token to nikgo nie obchodzi
if TOKEN:
    client.run(TOKEN)
#jest druga w nocy
#ide spać
#dobranoc