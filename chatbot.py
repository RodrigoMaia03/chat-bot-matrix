from nio import AsyncClient, RoomMessageText

# Substitua "SEU_ACCESS_TOKEN" pelo token da sua conta do bot
client = AsyncClient("https://matrix.org", "syt_Y2hhdGJvdHBpYmlj_iSNxEhejwAcjharwAQnw_4NsS2D")

# Função de resposta básica
async def message_callback(room, event):
    if isinstance(event, RoomMessageText):
        await client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"Você disse: {event.body}"}
        )

# Conecta e ouve eventos
async def main():
    client.add_event_callback(message_callback, RoomMessageText)
    await client.sync_forever(timeout=30000)  # Mantém sincronizado

import asyncio
asyncio.run(main())