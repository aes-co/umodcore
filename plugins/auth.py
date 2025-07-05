# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
from utils.core import (
    eor,
    register_command,
    handle_error,
    owner_only,
    add_sudo_user,
    remove_sudo_user,
    is_sudo_user,
    SUDO_USERS,
    OWNER_ID,
    delete_after
)

def register_auth(client: TelegramClient):
    @register_command(client, "auth", owner_only=True)
    @handle_error
    async def add_sudo(event):
        """Add user to sudo list (Owner only)"""
        try:
            # Get user from reply or mention
            user = None
            user_id = None
            
            # Check if replying to a message
            if event.reply_to_msg_id:
                reply_msg = await event.get_reply_message()
                if reply_msg and reply_msg.sender:
                    user = reply_msg.sender
                    user_id = reply_msg.sender_id
            
            # Check if user ID or username provided in command
            elif len(event.text.split()) > 1:
                user_input = event.text.split()[1]
                
                # If it's a number (user ID)
                if user_input.isdigit():
                    user_id = int(user_input)
                    try:
                        user = await client.get_entity(user_id)
                    except:
                        await eor(event, "❌ User ID tidak valid atau tidak ditemukan!")
                        return
                
                # If it's a username
                elif user_input.startswith('@'):
                    try:
                        user = await client.get_entity(user_input)
                        user_id = user.id
                    except:
                        await eor(event, "❌ Username tidak valid atau tidak ditemukan!")
                        return
                else:
                    try:
                        user = await client.get_entity(user_input)
                        user_id = user.id
                    except:
                        await eor(event, "❌ Username tidak valid atau tidak ditemukan!")
                        return
            
            if not user_id:
                await eor(event, "❌ **Cara penggunaan:**\n• Reply ke pesan user\n• `.auth @username`\n• `.auth user_id`")
                return
            
            # Check if user is already owner
            if user_id == OWNER_ID:
                await eor(event, "❌ Owner tidak perlu ditambahkan ke sudo!")
                return
            
            # Check if already sudo
            if is_sudo_user(user_id):
                user_name = user.first_name if user else "User"
                await eor(event, f"❌ {user_name} sudah menjadi sudo user!")
                return
            
            # Add to sudo
            await add_sudo_user(user_id)
            user_name = user.first_name if user else f"User {user_id}"
            
            msg = await eor(event, f"✅ **Sudo berhasil ditambahkan!**\n\n👤 User: {user_name}\n🆔 ID: `{user_id}`\n🔑 Status: Sudo User")
            await delete_after(msg, 30)
            
        except Exception as e:
            await eor(event, f"❌ Error: {str(e)}")
    
    @register_command(client, "deauth", owner_only=True)
    @handle_error
    async def remove_sudo(event):
        """Remove user from sudo list (Owner only)"""
        try:
            # Get user from reply or mention
            user = None
            user_id = None
            
            # Check if replying to a message
            if event.reply_to_msg_id:
                reply_msg = await event.get_reply_message()
                if reply_msg and reply_msg.sender:
                    user = reply_msg.sender
                    user_id = reply_msg.sender_id
            
            # Check if user ID or username provided in command
            elif len(event.text.split()) > 1:
                user_input = event.text.split()[1]
                
                # If it's a number (user ID)
                if user_input.isdigit():
                    user_id = int(user_input)
                    try:
                        user = await client.get_entity(user_id)
                    except:
                        pass  # User might not be accessible but we can still remove from sudo
                
                # If it's a username
                elif user_input.startswith('@'):
                    try:
                        user = await client.get_entity(user_input)
                        user_id = user.id
                    except:
                        await eor(event, "❌ Username tidak valid atau tidak ditemukan!")
                        return
                else:
                    try:
                        user = await client.get_entity(user_input)
                        user_id = user.id
                    except:
                        await eor(event, "❌ Username tidak valid atau tidak ditemukan!")
                        return
            
            if not user_id:
                await eor(event, "❌ **Cara penggunaan:**\n• Reply ke pesan user\n• `.deauth @username`\n• `.deauth user_id`")
                return
            
            # Check if user is owner
            if user_id == OWNER_ID:
                await eor(event, "❌ Owner tidak bisa dihapus dari sudo!")
                return
            
            # Check if user is sudo
            if not is_sudo_user(user_id):
                await eor(event, "❌ User tersebut bukan sudo user!")
                return
            
            # Remove from sudo
            await remove_sudo_user(user_id)
            user_name = user.first_name if user else f"User {user_id}"
            
            msg = await eor(event, f"✅ **Sudo berhasil dihapus!**\n\n👤 User: {user_name}\n🆔 ID: `{user_id}`\n🔑 Status: Regular User")
            await delete_after(msg, 30)
            
        except Exception as e:
            await eor(event, "❌ Terjadi kesalahan tak terduga. Insiden ini telah dicatat.")

    @register_command(client, "sudolist", owner_only=True)
    @handle_error
    async def list_sudo(event):
        """List all sudo users (Owner only)"""
        try:
            if not SUDO_USERS:
                await eor(event, "📝 **Daftar Sudo Users:**\n\n❌ Tidak ada sudo user yang terdaftar.")
                return
            
            sudo_list = "📝 **Daftar Sudo Users:**\n\n"
            
            for i, user_id in enumerate(SUDO_USERS, 1):
                try:
                    user = await client.get_entity(user_id)
                    name = user.first_name
                    username = f"@{user.username}" if user.username else "No username"
                    sudo_list += f"{i}. {name} ({username})\n   ID: `{user_id}`\n\n"
                except:
                    sudo_list += f"{i}. Unknown User\n   ID: `{user_id}`\n\n"
            
            sudo_list += f"📊 Total: {len(SUDO_USERS)} sudo users"
            
            msg = await eor(event, sudo_list)
            await delete_after(msg, 60)
            
        except Exception as e:
            await eor(event, "❌ Terjadi kesalahan tak terduga. Insiden ini telah dicatat.")

    @register_command(client, "reloadsudo", owner_only=True)
    @handle_error
    async def reload_sudo_users_command(event):
        """Reload sudo users from database (Owner only)"""
        from utils.core import load_sudo_users
        await load_sudo_users()
        await eor(event, "✅ Daftar sudo user berhasil dimuat ulang dari database.")
