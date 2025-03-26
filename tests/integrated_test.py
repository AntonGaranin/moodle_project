import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, User, Chat, KeyboardButton
from ..main import send_welcome, user_sessions


@pytest.fixture
async def cleanup_sessions():
    """Фикстура для очистки сессий"""
    user_sessions.clear()
    yield
    user_sessions.clear()


def create_test_message(user_id: int = 123, text: str = "/start"):
    """Создание тестового сообщения"""
    return MagicMock(
        spec=Message,
        message_id=1,
        from_user=User(id=user_id, first_name="Test", is_bot=False, username="test_user"),
        chat=Chat(id=123, type="private"),
        date=datetime.now(),
        text=text,
        answer=AsyncMock()
    )


@pytest.mark.asyncio
async def test_send_welcome_for_new_user(cleanup_sessions):
    """Тест для нового пользователя"""
    message = create_test_message()

    await send_welcome(message)

    # Проверяем создание сессии
    user_id = str(message.from_user.id)
    assert user_id in user_sessions

    # Проверяем начальное состояние
    session = user_sessions[user_id]
    assert session["username"] == ""
    assert session["password"] == ""

    # Проверяем клавиатуру
    btn_texts = [btn.text for btn in session["keyboard"]]
    assert "Новый пользователь" in btn_texts
    assert "Авторизация по данным" in btn_texts

    # Проверяем отправку сообщения
    message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_send_welcome_for_existing_user(cleanup_sessions):
    """Тест для существующего пользователя"""
    # Подготовка тестовых данных
    user_id = "123"
    user_sessions[user_id] = {
        "username": "test_user",
        "password": "test_pass",
        "keyboard": [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="Мои курсы")
        ],
        "payload": None,
        "courses_dict": None,
        "session": None
    }

    message = create_test_message(user_id=int(user_id))

    await send_welcome(message)

    # Проверяем, что данные не изменились
    assert user_sessions[user_id]["username"] == "test_user"

    # Проверяем клавиатуру
    btn_texts = [btn.text for btn in user_sessions[user_id]["keyboard"]]
    assert "Назад" in btn_texts
    assert "Мои курсы" in btn_texts

    # Проверяем отправку сообщения
    message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_send_welcome_multiple_users(cleanup_sessions):
    """Тест для нескольких пользователей"""
    message1 = create_test_message(user_id=111)
    message2 = create_test_message(user_id=222)

    await send_welcome(message1)
    await send_welcome(message2)

    # Проверяем создание отдельных сессий
    assert "111" in user_sessions
    assert "222" in user_sessions
    assert user_sessions["111"] is not user_sessions["222"]