import random
import firebase_admin
from firebase_admin import credentials, db
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🆔 Reemplaza con tu ID de Telegram
ADMIN_ID = 7628987708  # ← Cambia esto por tu ID real (usa /myid)

# 🔐 Inicializa Firebase
cred = credentials.Certificate("firebase-cred.json")  # ← Asegúrate que el archivo exista
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nequi-bot-da061-default-rtdb.firebaseio.com/'
})

# 🎲 Comando /generar (solo para el admin)
async def generar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 No tienes permiso para usar este comando.")
        return

    number = str(random.randint(3000000000, 3999999999))
    pin = str(random.randint(1000, 9999))
    ref = db.reference('users')
    ref.push({'number': number, 'pin': pin})
    await update.message.reply_text(f"✅ Número generado:\n📱 Número: {number}\n🔐 PIN: {pin}")

# 📌 Comando /myid para saber tu ID
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Tu ID es: {update.effective_user.id}")

# 🚀 Inicia el bot
app = ApplicationBuilder().token("8169621220:AAEkT35uQe5aN9apF7EF1P80mujh7pe5I4o").build()  # ← Reemplaza tu token real
app.add_handler(CommandHandler("generar", generar))
app.add_handler(CommandHandler("myid", myid))
app.run_polling()
