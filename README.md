# antworker

##  Стек технологий

- **[httpx](https://www.python-httpx.org/)** — асинхронный HTTP-клиент для Python. Быстрый и удобный инструмент для работы с HTTP-запросами.  
- **[pydantic](https://pydantic-docs.helpmanual.io/)** — библиотека для валидации и работы с данными, которая позволяет легко управлять типами данных и проверками.  
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — позволяет загружать переменные окружения из `.env` файла, что упрощает настройку проекта и работу с конфиденциальной информацией.  
- **[uv](https://docs.astral.sh/uv/)** — быстрый и надёжный менеджер зависимостей, который упрощает установку и управление библиотеками Python.  

###  Dev-зависимости

- **[mypy](https://mypy-lang.org/)** — статический анализатор типов.  
- **[ruff](https://docs.astral.sh/ruff/)** — быстрый линтер и автоформаттер.  
- **[flake8](https://flake8.pycqa.org/)** — инструмент для проверки качества кода.  
- **[pytest](https://docs.pytest.org/)** — фреймворк для написания и запуска тестов.  

---

## ⚙️ Установка и активация виртуального окружения

```bash
# Создать виртуальное окружение
uv venv

# Активация окружения:
source .venv/Scripts/activate        # Windows
source .venv/bin/activate            # WSL / Git Bash / Linux / macOS

# Установить зависимости проекта
uv pip install

# Установить dev-зависимости (опционально)
uv pip install .[dev]
