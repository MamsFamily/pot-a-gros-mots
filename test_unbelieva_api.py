import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

UNB_TOKEN = os.getenv("UNBELIEVABOAT_API_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
JAR_USER_ID = os.getenv("JAR_USER_ID")

async def main():
    if not all([UNB_TOKEN, GUILD_ID, JAR_USER_ID]):
        print("⚠️  Vérifie tes variables d'environnement :")
        print("   - UNBELIEVABOAT_API_TOKEN")
        print("   - GUILD_ID")
        print("   - JAR_USER_ID")
        return

    url = f"https://unbelievaboat.com/api/v1/guilds/{GUILD_ID}/users/{JAR_USER_ID}"
    headers = {"Authorization": UNB_TOKEN}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                print("✅ Connexion API réussie !")
                print(f"🏦 Utilisateur (ID: {JAR_USER_ID}) trouvé sur le serveur {GUILD_ID}.")
                print(f"💎 Solde actuel : {data.get('cash', 0)} cash | {data.get('bank', 0)} bank")
            elif resp.status == 404:
                print("❌ Le compte-jarre n'a pas été trouvé sur ton serveur.")
                print("   ➤ Vérifie que ce compte est bien présent et qu'il a déjà un solde UnbelievaBoat (via /balance).")
            elif resp.status == 401:
                print("❌ Jeton API invalide. Vérifie UNBELIEVABOAT_API_TOKEN dans tes secrets Replit.")
            else:
                text = await resp.text()
                print(f"⚠️ Réponse inattendue ({resp.status}) : {text}")

if __name__ == "__main__":
    asyncio.run(main())
