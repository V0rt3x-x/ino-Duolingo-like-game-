import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import time, random
from googletrans import Translator

duration = 5
sample_rate = 44100
codes = [
    "en - английский", 
    "es - испанский", 
    "pt - португальский", 
    "id - индонезийский", 
    "pl - польский", 
    "it - итальянский", 
    "tr - турецкий"
        ]
codes2 = ["en", "es", "pt", "id", "pl", "it", "tr"]
words = {
    "A1": ["привет", "пока", "спасибо", "пожалуйста", "друг", "дом", "школа", "книга", "вода", "еда"],
    "A2": ["время", "погода", "работа", "город", "деньги", "магазин", "билет", "поезд", "семья", "рыба"],
    "B1": ["успех", "решение", "опыт", "цель", "выбор", "закон", "мнение", "общество", "развитие", "качество"],
    "B2": ["влияние", "исследование", "ценность", "окружающая среда", "последствие", "способность", "улучшение", "справедливость", "возможность", "достижение"],
    "C1": ["осознание", "пренебрежение", "уязвимость", "противоречие", "устойчивость", "двусмысленность", "предвзятость", "заблуждение", "сплоченность", "красноречие"],
    "C2": ["безупречность", "неизбежность", "мировоззрение", "кратковременность", "проницательность", "сострадание", "утонченность", "многогранность", "непредсказуемость", "самопожертвование"]
}

def recording(duration, sample_rate):
    print(40*"-", "🎙 Говори...", sep='\n')
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()  # ждём завершения записи

    wav.write("output.wav", sample_rate, recording)
    print("✅ Запись завершена, теперь распознаём...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print("📝 Ты сказал:", text)
    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("❌ Не удалось распознать речь.")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"❌ Ошибка сервиса: {e}")
    print(" ")

    translator = Translator()
    while True:
        print(*codes, sep="\n")
        print(" ")
        dest = input('🔀 Выберите код языка, на который вы хотите перевести свою речь: en, es, pt, id, pl, it, tr: ')
        translated = translator.translate(text, dest)
        match dest:
            case 'en':
                print("🌍 Перевод на английский:", translated.text)
                break
            case "es":
                print("🌍 Перевод на испанский:", translated.text)
                break
            case 'pt':
                print("🌍 Перевод на португальский:", translated.text)
                break
            case "id":
                print("🌍 Перевод на индонейзиский:", translated.text)
                break
            case 'pl':
                print("🌍 Перевод на польский:", translated.text)
                break
            case "it":
                print("🌍 Перевод на итальянский:", translated.text)
                break
            case "tr":
                print("🌍 Перевод на турецкий:", translated.text)
                break
            case _:
                print("Вводимый вариант отсутствует, потворите попытку")
            

    print(40*"-")

def game():
    print(40*"-")
    # === Выбор уровня сложности ===
    print("👋 Приветствую тебя в нашей игре ino!")
    time.sleep(1)
    print("💪 Здесь ты сможешь проверить знание языка!")
    time.sleep(1)
    print("🚀 Поехали!")
    time.sleep(1)

    print(*codes, sep="\n")
    print(" ")
    time.sleep(0.5)
    dest = input('🔀 Выберите код языка, знание которого хочешь проверить: en, es, pt, id, pl, it, tr: ')
    while dest not in codes2:
        print("⚠️ Код не найден, повторите попытку")
        dest = input('🔀 Выберите код языка, знание которого хочешь проверить: en, es, pt, id, pl, it, tr: ')
    time.sleep(0.5)
    level = input("✍️ Выбери уровень сложности: A1, A2, B1, B2, C1, C2: ").strip().upper()
    while level not in words:
        print("⚠️ Уровень не найден, повторите попытку")
        level = input("✍️ Выбери уровень сложности: A1, A2, B1, B2, C1, C2: ").strip().upper()

    word_list_by_level = words[level]
    hp = 5
    points = 0
    random.shuffle(word_list_by_level)

    print("▶️ Ты увидишь слово на русском. Переведи его на выбранный язык за 5 секунд")
    time.sleep(1)
    print(" ")

    # === Инициализация инструментов ===
    recognizer = sr.Recognizer()
    translator = Translator()

    # === Основной игровой цикл ===
    for word in word_list_by_level:
        print(40*"-")
        time.sleep(0.3)
        print("🔈 Слово:", word)
        time.sleep(0.3)
        print("🎙 Говори...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
        sd.wait()  # ждём завершения записи
        time.sleep(0.3)

        wav.write("output.wav", sample_rate, recording)
        print("✅ Запись завершена, теперь распознаём...")
        time.sleep(0.3)

        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            recognized = recognizer.recognize_google(audio, language=dest).strip().lower()
            print("📝 Ты сказал:", recognized)
            time.sleep(0.3)

            translation = translator.translate(word, dest, src="ru").text.strip().lower()
            print(f"🔠 Перевод: {translation}")
            time.sleep(0.3)

            if recognized == translation:
                points += 1
                print("✅ Верно! +1 балл")
                time.sleep(0.3)
            else:
                hp -= 1
                print(f"❌ Неверно! Правильный ответ: {translation}")
                time.sleep(0.3)
                print(f"❤️ Текущее количество hp: {hp}")
                time.sleep(0.3)
            if hp <= 0:
                print("💀 Игра окончена! Ты допустил 5 ошибок 💀")
                time.sleep(0.3)
                print(40*"-")
                break
        except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
            hp -= 1
            print(f"❌ Не удалось распознать речь. Правильный ответ: {translation}")
            time.sleep(0.3)
            print(f"❤️ Текущее количество hp: {hp}")
            time.sleep(0.3)

            if hp <= 0:
                print("💀 Игра окончена! Ты допустил 5 ошибок 💀")
                time.sleep(0.3)
                print(40*"-")
                break
        except sr.RequestError as e:             # - если нет интернета или API недоступен
            print(f"❌ Ошибка сервиса: {e}")
            break
        print(" ")

    # === Итоги ===
    if not hp <= 0:
        print(f"🏁 Игра окончена! Набрано баллов: {points} из 10 🏆")
        time.sleep(0.3)
        print(40*"-")