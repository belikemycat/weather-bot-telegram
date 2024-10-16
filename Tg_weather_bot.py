import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import time
API_KEY = "YOUR BOT'S TOKEN!"
WEATHER_API_KEY = "3bc309f50c8c26fb6ff56420c3d2fadf"

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['cod'] == 200:
            return display_weather(data)
        else:
            return "Oops...city was not found 🔍"
    except requests.exceptions.RequestException as e:
        return "Oops...city was not found 🔍"

def display_weather(data):
    temperature_k = data["main"]["temp"]
    weather_description = data["weather"][0]["description"]
    temperature_c = temperature_k - 273.15
    weather_id = data["weather"][0]["id"]

    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]
    current_time = time.time()

    # if day then bright emojis !))
    is_daytime = sunrise <= current_time <= sunset

    weather_emoji = get_weather_icon(weather_id, is_daytime)
    return f'{temperature_c:.1f}°C {weather_emoji}\n{weather_description}'

# this is how we get the emojis for weather, depending on weather_id
def get_weather_icon(weather_id, is_daytime):
    if 200 <= weather_id <= 232:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "☁️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif  600 <= weather_id <= 622:
        return "❄️"
    elif 701 <= weather_id <= 741:
        return "🌫️"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "🌬️"
    elif weather_id == 781:
        return "🌪️"
    elif weather_id == 800:
        return "☀️" if is_daytime else "🌑"  
    elif 801 <= weather_id <= 804:
        return "⛅" if is_daytime else "☁️" 
    else:
        return "🌡️"

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text('Hello! Send me a city name to get the weather 🌡️')

# Обработчик текстовых сообщений (название города)
async def handle_message(update: Update, context):
    city = update.message.text
    weather_info = get_weather(city)
    if weather_info:
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Sorry, no weather information available.")

def main():
    application = Application.builder().token(API_KEY).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
