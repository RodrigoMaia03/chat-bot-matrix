from dotenv import load_dotenv
import os
import nio
import asyncio

class ChatBot:
    def __init__(self, homeserver, user_id, access_token):
        self.client = nio.AsyncClient(homeserver, user_id, store_path="./store")
        self.client.access_token = access_token
        self.last_event_id = None
        self.initial_sync_done = False

    async def message_callback(self, room, event):
        if isinstance(event, nio.RoomMessageText) and event.sender != self.client.user_id:
            if self.initial_sync_done and self.last_event_id != self.client.user_id:
                response = f"Você disse: {event.body}"
                await self.client.room_send(
                    room.room_id,
                    message_type="m.room.message",
                    content={
                        "msgtype": "m.text",
                        "body": response,
                    }
                )
                self.last_event_id = self.client.user_id  # Atualiza o ID do último evento processado
            else:
                self.last_event_id = None

    async def initial_sync(self):
        # Faz a sincronização inicial e ignora todas as mensagens recebidas anteriormente
        response = await self.client.sync()
        self.initial_sync_done = True

    async def main(self):
        self.client.add_event_callback(self.message_callback, nio.RoomMessageText)
        await self.initial_sync()  # Faz a sincronização inicial
        await self.client.sync_forever(10000)  # Continua sincronizando para novas mensagens

if __name__ == "__main__":
    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv(dotenv_path= 'C:/Users/lc18v/Documents/PIBIC/Infos/chatbot/config.env')
    
    # Configurações do bot
    HOMESERVER = os.getenv("HOMESERVER")
    USER_ID = os.getenv("USER_ID")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

    bot = ChatBot(HOMESERVER, USER_ID, ACCESS_TOKEN)
    
    # Executa o bot
    asyncio.run(bot.main())