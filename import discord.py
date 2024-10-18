import discord
from discord.ext import commands
import os
import base64 as b64
from PIL import Image
import asyncio
import subprocess
import shutil

intents = discord.Intents.default()
intents.messages = True  # Üzenetek kezelése
intents.message_content = True  # Üzenetek tartalmának elérése
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ID: {bot.user.id}")
    print(f"Bot Username: {bot.user.name}")
    print(f"Bot Discriminator: {bot.user.discriminator}")
    print(f"Bot Avatar URL: {bot.user.avatar.url}")  # Használj 'bot.user.avatar.url'-t
    print(f"Is Bot: {bot.user.bot}")

# Parancs, ami elküldi a fájlokat egy adott mappából, ha kisebbek 10 MB-nál
@bot.command()
async def f(ctx, folder_path: str, *file_names: str):
    max_size = 10 * 1024 * 1024  # 10 MB, byte-ban

    if not os.path.exists(folder_path):
        await ctx.send(f"A mappa nem található: {folder_path}")
        return

    if file_names:
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and os.path.getsize(file_path) < max_size:
                try:
                    await ctx.send(file=discord.File(file_path))
                except Exception as e:
                    await ctx.send(f"Nem sikerült elküldeni a fájlt: {file_name}. Hiba: {e}")
            else:
                await ctx.send(f"A fájl nem található vagy nagyobb, mint 10 MB: {file_name}")
    else:
        await ctx.send("Kérlek, adj meg fájlneveket a fájlok elküldéséhez.")

@bot.command()
async def nigger(ctx):
    await ctx.reply(r""" kys budos nigger """)

@bot.command()
async def base64(ctx, action: str, *, text: str):
    if action == 'e':  # Kódolás
        encoded_text = b64.b64encode(text.encode('utf-8')).decode('utf-8')
        await ctx.reply(f"Base64 kódolt: {encoded_text}", mention_author=True)
    elif action == 'd':  # Dekódolás
        try:
            decoded_text = b64.b64decode(text).decode('utf-8')
            await ctx.reply(f"Base64 dekódolt: {decoded_text}", mention_author=True)
        except Exception as e:
            await ctx.reply(f"Hiba a dekódolás során: {e}", mention_author=True)
    else:
        await ctx.reply("Kérlek, add meg az 'e' (kódolás) vagy 'd' (dekódolás) argumentumot.", mention_author=True)

def create_gif(image_path, output_gif_path):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    piece_width = width // 4  # A kép negyedének szélessége
    piece_height = height // 4  # A kép negyedének magassága

    frames = []
    for i in range(4):
        for j in range(4):
            left = j * piece_width
            upper = i * piece_height
            right = left + piece_width
            lower = upper + piece_height
            piece = image.crop((left, upper, right, lower))
            
            # Kép létrehozása a kép negyedének megfelelő méretben
            clear_frame = Image.new("RGBA", (piece_width, piece_height), (255, 255, 255, 0))
            clear_frame.paste(piece, (0, 0))  # Blokk hozzáadása
            frames.append(clear_frame)

    # GIF létrehozása az összes frame-ből
    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], duration=100, loop=0, disposal=2)

@bot.command()
async def kep(ctx):
    if not ctx.message.attachments:
        await ctx.reply("Nem csatoltál képfájlt.")
        return

    for attachment in ctx.message.attachments:
        if not attachment.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            await ctx.reply(f"{attachment.filename} nem PNG vagy JPG fájl, ezt kihagyom.")
            continue

        try:
            image_path = os.path.join(os.getcwd(), attachment.filename)
            await attachment.save(image_path)

            # Kép fájlnevéből kivesszük a kiterjesztést, és hozzáadjuk a .gif kiterjesztést
            base_filename = os.path.splitext(attachment.filename)[0]
            output_gif_path = os.path.join(os.getcwd(), f"{base_filename}.gif")
            
            create_gif(image_path, output_gif_path)
            
            await ctx.reply(file=discord.File(output_gif_path))
            
            os.remove(image_path)
            os.remove(output_gif_path)
        
        except Exception as e:
            await ctx.reply(f"Hiba történt a {attachment.filename} GIF készítése során: {e}")
        
        # Várakozás a fájlok feldolgozása között
        await asyncio.sleep(1)



@bot.command()
async def letoltesek(ctx):
    try:
        command = f'C:\\Users\\Gergő\\Downloads\\platform-tools-latest-windows\\platform-tools\\adb shell ls /sdcard/Download'
        output = subprocess.check_output(command, shell=True, text=True, errors='replace')
        files = output.splitlines()

        if not files:
            await ctx.send("Nincsenek fájlok a letöltések mappájában.")
            return

        message = "A letöltések mappájában lévő fájlok:\n"
        for file in files:
            if len(message) + len(file) + 2 > 2000:  # +2 a newline karakterek miatt
                await ctx.send(message)
                message = "A letöltések mappájában lévő fájlok:\n"  # Üzenet újraindítása
            message += f"{file}\n"

        if message:  # Az utolsó üzenet küldése
            await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Hiba történt a letöltés során: {str(e)}")

@bot.command()
async def fa(ctx, *file_names: str):
    try:
        download_path = 'C:\\Users\\Gergő\\Downloads\\'
        temp_path = os.path.join(download_path, 'temp')
        
        # Ideiglenes mappa létrehozása, ha nem létezik
        os.makedirs(temp_path, exist_ok=True)

        response_messages = []

        for file_name in file_names:
            local_file_path = os.path.join(temp_path, file_name)

            if os.path.isfile(local_file_path):
                response_messages.append(f"Elküldve: {file_name}")
                await ctx.send(file=discord.File(local_file_path))
            else:
                adb_command = f'C:\\Users\\Gergő\\Downloads\\platform-tools-latest-windows\\platform-tools\\adb pull /sdcard/Download/{file_name} "{local_file_path}"'
                subprocess.check_output(adb_command, shell=True)

                if os.path.isfile(local_file_path):
                    response_messages.append(f"Elküldve: {file_name}")
                    await ctx.send(file=discord.File(local_file_path))
                else:
                    response_messages.append(f"A '{file_name}' fájl nem található a letöltések mappájában.")

        await ctx.send("\n".join(response_messages))

        # Ideiglenes fájlok törlése
        shutil.rmtree(temp_path)

    except Exception as e:
        await ctx.send(f"Hiba történt a fájl keresése során: {str(e)}")


@bot.command()
async def base64_convert(ctx, *, message: str):
    encoded_message = b64.b64encode(message.encode('utf-8')).decode('utf-8')

    for i in range(10):  # 10 ciklus
        await ctx.send(f"{i+1}. Base64 verzió: {encoded_message}")
        encoded_message = b64.b64encode(encoded_message.encode('utf-8')).decode('utf-8')

    await ctx.send(f"Végső Base64 üzenet: {encoded_message}")

@bot.command()
async def base64_decode(ctx, *, encoded_message: str):
    decoded_message = encoded_message
    for _ in range(11):  # Dekódolás 10 ciklusban
        # Helyes padding hozzáadása dekódolás előtt
        padded_message = decoded_message + '=' * (-len(decoded_message) % 4)
        decoded_message = b64.b64decode(padded_message.encode('utf-8')).decode('utf-8')
        await ctx.send(f"Eredeti üzenet: {decoded_message}")







def string_to_hex(message: str) -> str:
    return ''.join(format(ord(char), '02x') for char in message)

def hex_to_string(hex_message: str) -> str:
    decoded_message = ''
    for i in range(0, len(hex_message), 2):
        byte = hex_message[i:i+2]
        decoded_message += chr(int(byte, 16))
    return decoded_message

@bot.command()
async def hex_convert(ctx, *, message: str):
    # Az első hexadecimális konverzió
    hex_message = string_to_hex(message)

    # Minden ciklusban újrakonvertáljuk az előző hexadecimális üzenetet
    for i in range(5):
        # Küldés a jelenlegi hexadecimális üzenetről
        await ctx.send(f"{i+1}. Hexadecimális verzió: {hex_message}")
        
        # Az újonnan kódolt üzenetet újra hexadecimális formátumba konvertáljuk
        hex_message = string_to_hex(hex_message)

    # Visszafejtjük az utolsó hexadecimális üzenetet karakterekké
    decoded_message = ''
    for i in range(0, len(hex_message), 2):
        byte = hex_message[i:i+2]
        decoded_message += chr(int(byte, 16))

    # Eredeti üzenet küldése válaszként
    await ctx.send(f"Eredeti üzenet: {decoded_message}")
    
    # Válasz magának a botnak
    await ctx.reply(f"Megismételt üzenet: {decoded_message}")


@bot.command()
async def hex_decode(ctx, *, hex_message: str):
    decoded_message = hex_message
    for _ in range(5):  # Visszafejtés 5 ciklusban
        await ctx.send(f"{decoded_message}")
        decoded_message = hex_to_string(decoded_message)
        

    await ctx.send(f"Eredeti üzenet: {decoded_message}")


@bot.event
async def on_message(message):
    # Csak akkor lépjünk tovább, ha nem a bot küldte az üzenetet
    if message.author == bot.user:
        return

    # Prefix ellenőrzése és fájlnév megkeresése az üzenetben
    if message.content.startswith('!'):
        file_name = message.content[1:].strip()  # A prefix eltávolítása és a fájlnév megszerzése
        folder_path = r"C:\Users\Gergő\Downloads\cs\Download"  # Alapértelmezett mappa

        # Fájl útvonal összerakása
        file_path = os.path.join(folder_path, file_name)

        # Ellenőrizzük, hogy a fájl létezik-e és kisebb-e 10 MB-nál
        max_size = 10 * 1024 * 1024  # 10 MB, byte-ban
        if os.path.isfile(file_path) and os.path.getsize(file_path) < max_size:
            try:
                # Fájl küldése
                await message.channel.send(file=discord.File(file_path))
            except Exception as e:
                await message.channel.send(f"Nem sikerült elküldeni a fájlt: {file_name}. Hiba: {e}")
        else:
            await message.channel.send(f"A fájl nem található vagy nagyobb, mint 10 MB: {file_name}")

    # Parancsok további feldolgozása
    await bot.process_commands(message)

@bot.command()
async def convert(ctx):
    if not ctx.message.attachments:
        await ctx.send("Kérlek, csatolj egy MP4 fájlt.")
        return

    attachment = ctx.message.attachments[0]

    if attachment.size > 8 * 1024 * 1024:  # 8 MB
        await ctx.send("A fájl túl nagy. Kérlek, csatolj egy 8 MB-nál kisebb MP4 fájlt.")
        return

    input_file = f"C:\\Users\\Gergő\\Desktop\\Újmappa\\folders\\Új mappa\\{attachment.filename}"
    output_dir = os.path.splitext(input_file)[0]  # Kimeneti mappa
    output_m3u8 = os.path.join(output_dir, f"{attachment.filename[:-4]}.m3u8")

    # Fájl letöltése
    await attachment.save(input_file)

    if not os.path.exists(input_file):
        await ctx.send("A fájl letöltése sikertelen.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # HLS konvertálás
    hls_time = 1
    command = [
        'ffmpeg',
        '-i', input_file,
        '-codec', 'copy',
        '-start_number', '0',
        '-hls_time', str(hls_time),
        '-hls_list_size', '0',
        '-f', 'hls',
        output_m3u8
    ]
    
    # Futtatás és ellenőrzés
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        await ctx.send("Hiba történt a konvertálás során:\n" + result.stderr)
        return

    # TS fájlok elküldése
    ts_files = []
    for ts_file in os.listdir(output_dir):
        if ts_file.endswith('.ts'):
            ts_files.append(ts_file)
            await ctx.send(file=discord.File(os.path.join(output_dir, ts_file)))

    # Ellenőrizzük, hogy az M3U8 fájl létezik-e
    if os.path.exists(output_m3u8):
        await ctx.send(file=discord.File(output_m3u8))
    else:
        await ctx.send("Az M3U8 fájl nem jött létre.")

    await ctx.send("A konvertálás befejeződött.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.reference:
        referenced_message = await message.channel.fetch_message(message.reference.message_id)

        if referenced_message.attachments:
            file = referenced_message.attachments[0]  # Az első csatolt fájl

            if message.content.startswith('q encode'):
                await file.save(file.filename)

                # Read the uploaded file
                with open(file.filename, 'rb') as f:
                    file_bytes = f.read()

                # Encode the file content to Base64
                base64_text = b64.b64encode(file_bytes).decode('utf-8')

                # Create a new filename for the encoded file
                output_filename = f"{os.path.splitext(file.filename)[0]}.txt"

                # Save the Base64 encoded text to a new file
                with open(output_filename, 'w', encoding='utf-8') as output_file:
                    output_file.write(base64_text)

                # Send the encoded file back to the user
                await message.channel.send(file=discord.File(output_filename))

                # Optional: Remove the file after sending
                os.remove(output_filename)

            elif message.content.startswith('q decode'):
                await file.save(file.filename)

                # Read the uploaded Base64 encoded file
                with open(file.filename, 'r', encoding='utf-8') as f:
                    base64_text = f.read()

                # Decode the Base64 text
                decoded_bytes = b64.b64decode(base64_text)

                # Create a new file name (without .txt extension)
                output_filename = os.path.splitext(file.filename)[0]

                # Save the decoded bytes to a file
                with open(output_filename, 'wb') as output_file:
                    output_file.write(decoded_bytes)

                # Send the decoded file back to the user
                await message.channel.send(file=discord.File(output_filename))

                # Optional: Remove the file after sending
                os.remove(output_filename)

    # Process commands after handling the message
    await bot.process_commands(message)



        
# Bot indítása
bot.run('MTE1MDA1Nzc3ODc1NzUwMTA3OQ.GzbQAw.3_tMwrF9AUJFckj74r8PRUVzvgOJg0FFqm_PGo')
