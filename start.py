import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait, ChatAdminRequired, ChannelPrivate
from config import START_PIC, START_MSG, HELP_TXT, COMMAND_TXT, OWNER_ID, FSUB_CHANNEL, FSUB_CHANNEL_2, FSUB_CHANNEL_3

# Import database functions
from database import users_collection, save_broadcast_stats

# Bot start time for uptime calculation
BOT_START_TIME = None

def set_bot_start_time():
    """Set bot start time (call this when bot starts)"""
    import time
    global BOT_START_TIME
    BOT_START_TIME = time.time()

# --- UPDATED MULTI-CHANNEL FORCE SUBSCRIBE CHECKER ---
async def is_subscribed(client, message):
    # Filter out zero/empty channel IDs
    channels = []
    if FSUB_CHANNEL and FSUB_CHANNEL != 0:
        channels.append(FSUB_CHANNEL)
    if FSUB_CHANNEL_2 and FSUB_CHANNEL_2 != 0:
        channels.append(FSUB_CHANNEL_2)
    if FSUB_CHANNEL_3 and FSUB_CHANNEL_3 != 0:
        channels.append(FSUB_CHANNEL_3)
    
    # If no channels are configured, allow access
    if not channels:
        return True
    
    unjoined_channels = []
    channel_info_list = []
    
    # Check each channel
    for channel_id in channels:
        try:
            user = await client.get_chat_member(channel_id, message.from_user.id)
            if user.status == "kicked":
                await message.reply_text("<blockquote><b>❌ You are banned from using this bot.</b></blockquote>")
                return False
        except UserNotParticipant:
            # Get channel info
            try:
                chat = await client.get_chat(channel_id)
                channel_url = chat.invite_link if chat.invite_link else f"https://t.me/{chat.username}"
                unjoined_channels.append({
                    "id": channel_id,
                    "title": chat.title,
                    "url": channel_url
                })
                channel_info_list.append(f"• {chat.title}")
            except Exception as e:
                print(f"Error getting chat info: {e}")
                continue
        except Exception as e:
            print(f"FSub Error for {channel_id}: {e}")
            continue
    
    # If user hasn't joined all channels, show the requirement message
    if unjoined_channels:
        buttons = []
        for idx, channel in enumerate(unjoined_channels, 1):
            buttons.append([InlineKeyboardButton(f"Join Channel {idx} 📢", url=channel["url"])])
        
        # Add Try Again button
        buttons.append([InlineKeyboardButton("Try Again 🔄", callback_data="check_fsub")])
        
        channels_list = "\n".join(channel_info_list)
        await message.reply_text(
            f"<blockquote><b>⚠️ Force Subscribe Required!</b></blockquote>\n\n"
            f"<blockquote>Please join all these channels to use the bot:\n\n"
            f"{channels_list}\n\n"
            f"After joining, click 'Try Again'</blockquote>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return False
            
    return True

async def safe_edit(message, text, reply_markup=None):
    """Safely edit a message, ignoring 'MESSAGE_NOT_MODIFIED' errors"""
    try:
        await message.edit_text(text=text, reply_markup=reply_markup)
    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" not in str(e):
            raise e

def setup_start_handlers(app):
    """Register all start and related handlers"""
    
    @app.on_message(filters.command("start"))
    async def start_command(client, message):
        if not await is_subscribed(client, message):
            return

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs", callback_data="all_cmds")],
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/N4_Bots")],
            [
                InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="help")
            ]
        ])

        await client.send_photo(
            chat_id=message.chat.id,
            photo=START_PIC,
            caption=START_MSG,
            reply_markup=buttons
        )

    @app.on_callback_query()
    async def cb_handler(client, query: CallbackQuery):
        data = query.data
        user_id = query.from_user.id
        
        # --- FIX FOR UnboundLocalError: Extract target_user_id for LS-related callbacks ---
        if data.startswith(("ls_chat_", "ls_channel_", "ls_close_")):
            try:
                target_user_id = int(data.split("_")[2])
            except (IndexError, ValueError):
                await query.answer("Invalid callback data.", show_alert=True)
                return

        # ---------------- FORCE SUBSCRIBE RECHECK ----------------
        if data == "check_fsub":
            channels = []
            if FSUB_CHANNEL and FSUB_CHANNEL != 0:
                channels.append(FSUB_CHANNEL)
            if FSUB_CHANNEL_2 and FSUB_CHANNEL_2 != 0:
                channels.append(FSUB_CHANNEL_2)
            if FSUB_CHANNEL_3 and FSUB_CHANNEL_3 != 0:
                channels.append(FSUB_CHANNEL_3)

            unjoined_channels = []
            channel_info_list = []

            for channel_id in channels:
                try:
                    user = await client.get_chat_member(channel_id, user_id)
                    if user.status == "kicked":
                        await query.answer("You are banned from using this bot!", show_alert=True)
                        return
                except UserNotParticipant:
                    try:
                        chat = await client.get_chat(channel_id)
                        url = chat.invite_link if chat.invite_link else f"https://t.me/{chat.username}"
                        unjoined_channels.append({"title": chat.title, "url": url})
                        channel_info_list.append(f"• {chat.title}")
                    except:
                        continue

            if unjoined_channels:
                buttons = []
                for i, ch in enumerate(unjoined_channels, 1):
                    buttons.append(
                        [InlineKeyboardButton(f"Join Channel {i} 📢", url=ch["url"])]
                    )
                buttons.append(
                    [InlineKeyboardButton("Try Again 🔄", callback_data="check_fsub")]
                )
                
                channels_list = "\n".join(channel_info_list)
                
                await safe_edit(
                    query.message,
                    f"<b>⚠️ Still Not Subscribed!</b>\n\n"
                    f"<blockquote>You need to join all these channels:\n\n"
                    f"{channels_list}\n\n"
                    f"Please join and try again.</blockquote>",
                    InlineKeyboardMarkup(buttons)
                )
            else:
                await query.message.delete()
                await client.send_photo(
                    user_id,
                    START_PIC,
                    START_MSG,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs", callback_data="all_cmds")],
                        [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/N4_Bots")],
                        [
                            InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="help")
                        ]
                    ])
                )
            return

        # ---------------- MY ALL COMMANDS ----------------
        elif data == "all_cmds":
            # Update COMMAND_TXT to include /ls and /sf
            updated_command_txt = COMMAND_TXT + "\n<blockquote>• /ls - Sequence files from channel links (range selection)</blockquote>"
            
            await safe_edit(
                query.message,
                updated_command_txt,
                InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_start"),
                        InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")
                    ]
                ])
            )

        # ---------------- BACK → START ----------------
        elif data == "back_start":
            await safe_edit(
                query.message,
                START_MSG,
                InlineKeyboardMarkup([
                    [InlineKeyboardButton("ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs", callback_data="all_cmds")],
                    [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/N4_Bots")],
                    [
                        InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                        InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="help")
                    ]
                ])
            )

        # ---------------- ABOUT ----------------
        elif data == "help":
            await safe_edit(
                query.message,
                HELP_TXT,
                InlineKeyboardMarkup([
                    [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_start")]
                ])
            )

        # ---------------- CLOSE ----------------
        elif data == "close":
            await query.message.delete()

    @app.on_message(filters.command("leaderboard"))
    async def leaderboard(client, message):
        if not await is_subscribed(client, message):
            return
            
        from database import get_top_users
        top_users = get_top_users(5)
        text = "<blockquote>🏆 ᴛᴏᴘ ᴜsᴇʀs</blockquote>\n\n"
        for i, u in enumerate(top_users, 1):
            text += f"<blockquote>**{i}. {u.get('username', 'User')}** - {u.get('files_sequenced', 0)} files\n</blockquote>"
        await message.reply_text(text)

    @app.on_message(filters.command("status") & filters.user(OWNER_ID))
    async def simple_status_command(client, message):
        if not await is_subscribed(client, message):
            return
        
        import time
        from database import get_total_users
        
        total_users = get_total_users()
        
        # Uptime calculation
        if BOT_START_TIME:
            current_time = time.time()
            uptime_seconds = int(current_time - BOT_START_TIME)
            days, remainder = divmod(uptime_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            uptime_str = ""
            if days > 0:
                uptime_str += f"{days}d"
            if hours > 0:
                uptime_str += f"{hours}h"
            if minutes > 0:
                uptime_str += f"{minutes}m"
            uptime_str += f"{seconds}s"
        else:
            uptime_str = "Not set"
        
        # Ping calculation
        start_time = time.time()
        status_msg = await message.reply_text("<blockquote>Checking ping...</blockquote>")
        end_time = time.time()
        ping_ms = round((end_time - start_time) * 1000, 3)
        
        status_text = (
            f"<b>🤖 Bot Status</b>\n\n"
            f"<blockquote>⌚️ Bot Uptime : {uptime_str}\n"
            f"🐌 Current Ping : {ping_ms} ms\n"
            f"👭 Total Users : {total_users}</blockquote>"
        )
        
        await status_msg.edit_text(status_text)

    @app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
    async def simple_broadcast_command(client, message):
        if not message.reply_to_message:
            await message.reply_text(
                "<blockquote><b>❌ Please reply to a message to broadcast!</b></blockquote>\n"
                "<blockquote>Usage:\n1. Send a message\n"
                "2. Reply with /broadcast</blockquote>"
            )
            return
        
        # Direct broadcast without confirmation
        await message.reply_text("<blockquote>📤 Starting broadcast... Please wait.</blockquote>")
        
        from database import get_all_users
        all_users = get_all_users()
        total_users = len(all_users)
        
        success = 0
        failed = 0
        blocked = 0
        
        for user in all_users:
            user_id = user.get("user_id")
            
            try:
                await message.reply_to_message.copy(user_id)
                success += 1
                await asyncio.sleep(0.1)
                
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                try:
                    await message.reply_to_message.copy(user_id)
                    success += 1
                except:
                    failed += 1
                    
            except Exception as e:
                if "USER_IS_BLOCKED" in str(e) or "user is deactivated" in str(e):
                    blocked += 1
                else:
                    failed += 1
        
        # Save broadcast stats
        save_broadcast_stats(total_users, success, failed, blocked)
        
        stats_text = (
            f"<b>📊 Broadcast Completed!</b>\n\n"
            f"<blockquote>👥 Total Users: {total_users}\n"
            f"✅ Successful: {success}\n"
            f"❌ Failed: {failed}\n"
            f"🚫 Blocked/Deleted: {blocked}</blockquote>"
        )
        
        await message.reply_text(stats_text)

    # ---------- BROADCAST CALLBACK HANDLERS ----------
    @app.on_callback_query(filters.regex("confirm_broadcast|cancel_broadcast"))
    async def broadcast_callback_handler(client, query):
        data = query.data
        user_id = query.from_user.id
        
        if data == "confirm_broadcast":
            if user_id != OWNER_ID:
                await query.answer("Only owner can broadcast!", show_alert=True)
                return
            
            await query.message.edit_text("<blockquote>📤 Starting broadcast... Please wait.</blockquote>")
            
            # Get all users
            from database import get_all_users
            all_users = get_all_users()
            total_users = len(all_users)
            
            success = 0
            failed = 0
            blocked = 0
            
            # Start broadcasting
            progress_msg = await query.message.edit_text(
                f"<blockquote>📤 Broadcasting...\n"
                f"Progress: 0/{total_users}\n"
                f"✅ Success: 0 | ❌ Failed: 0</blockquote>"
            )
            
            for index, user in enumerate(all_users, 1):
                user_id = user.get("user_id")
                
                try:
                    await query.message.reply_to_message.copy(user_id)
                    success += 1
                    
                    if index % 20 == 0 or index == total_users:
                        try:
                            await progress_msg.edit_text(
                                f"<blockquote>📤 Broadcasting...\n"
                                f"Progress: {index}/{total_users}\n"
                                f"✅ Success: {success} | ❌ Failed: {failed}</blockquote>"
                            )
                        except:
                            pass
                    
                    await asyncio.sleep(0.1)
                    
                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                    try:
                        await query.message.reply_to_message.copy(user_id)
                        success += 1
                    except:
                        failed += 1
                        
                except Exception as e:
                    if "USER_IS_BLOCKED" in str(e) or "user is deactivated" in str(e):
                        blocked += 1
                    else:
                        failed += 1
            
            # Save broadcast stats
            save_broadcast_stats(total_users, success, failed, blocked)
            
            # Send final stats
            stats_text = (
                f"<b>📊 Broadcast Completed!</b>\n\n"
                f"<blockquote>👥 Total Users: {total_users}\n"
                f"✅ Successful: {success}\n"
                f"❌ Failed: {failed}\n"
                f"🚫 Blocked/Deleted: {blocked}</blockquote>"
            )
            
            await progress_msg.edit_text(stats_text)
        
        elif data == "cancel_broadcast":
            await query.message.edit_text("<blockquote>❌ Broadcast cancelled.</blockquote>")
