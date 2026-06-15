# Импорт и инициализация
from flask import Flask, render_template, request
app = Flask(__name__)
# Словарь памятных событий
events = {
    "1.1": "Новый год",
    "7.1": "Рождество Христово (православное)",
    "23.2": "День защитника Отечества",
    "8.3": "Международный женский день",
    "1.5": "Праздник Весны и Труда",
    "9.5": "День Победы",
    "12.6": "День России",
    "4.11": "День народного единства",
    "12.4": "День космонавтики",
    "27.5": "День библиотек",
    "1.6": "День защиты детей",
    "22.8": "День Государственного флага РФ",
    "1.9": "День знаний",
    "5.10": "День учителя",
}
def get_event(day, month):
    # Возвращает событие для заданного дня и месяца
    try:
        # Приводим к целым
        day_int = int(day)
        month_int = int(month)
        # Формируем ключ в формате "день, месяц"
        key = f"{day_int}.{month_int}"
        # Ищем событие в словаре
        return events.get(key, None)
    except (ValueError, TypeError):
        # Сработает, если day или month нельзя преобразовать в число
        return None
@app.route("/", methods=["GET", "POST"])
def index():
    # Словарь для отслеживания ошибок
    error = {
        "day_error": False,
        "month_error": False
    }
    event = None
    if request.method == "POST":
        day = request.form.get("day")
        month = request.form.get("month")
        # Проверяем день (от 1 до 31)
        try:
            day_val = int(day)
            if day_val < 1 or day_val > 31:
                error["day_error"] = True
                day_val = None
        except (ValueError, TypeError):
            error["day_error"] = True
            day_val = None
        # Проверяем месяц (от 1 до 12)
        try:
            month_val = int(month)
            if month_val < 1 or month_val > 12:
                error["month_error"] = True
                month_val = None
        except (ValueError, TypeError):
            error["month_error"] = True
            month_val = None
        # Если ошибок нет, ищем событие
        if not error["day_error"] and not error["month_error"]:
            event = get_event(day_val, month_val)
            # Если событие не найдено
            if event is None:
                error["not_found"] = True
        else:
            # Если были ошибки ввода
            error["not_found"] = False
    # Показываем страницу пользователю с формой и результатом поиска
    return render_template("index.html", error=error, event=event)
if __name__ == "__main__":
    app.run() #Запуск