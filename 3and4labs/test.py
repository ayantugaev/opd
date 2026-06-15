# Импортируем модуль app, из которого будем тестировать функцию get_event
import app
# Импортируем стандартную библиотеку unittest
import unittest
class TestApp(unittest.TestCase):
    # Тесты для функции get_event
    # Тест 1: Проверка существующего события (12 апреля - День космонавтики)
    def test_event_1(self):
        event = app.get_event(12, 4)
        self.assertEqual(event, "День космонавтики")
    # Тест 2: Проверка второго существующего события (9 мая - День Победы)
    def test_event_2(self):
        event = app.get_event(9, 5)
        self.assertEqual(event, "День Победы")
    # Тест 3: Проверка даты с ведущими нулями (01.01 - Новый год)
    def test_event_3(self):
        event = app.get_event("01", "01")
        self.assertEqual(event, "Новый год")
    # Тест 4: Все входные данные равны None
    def test_event_none(self):
        event = app.get_event(None, None)
        self.assertIsNone(event)
    # Тест 5: Проверка несуществующей даты (8 февраля)
    def test_event_not_found(self):
        event = app.get_event(8, 2)
        self.assertIsNone(event)
if __name__ == "__main__":
    unittest.main()