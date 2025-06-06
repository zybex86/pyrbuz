# Testing and Linting Suika Game

This project uses [pytest](https://pytest.org/) for automated testing and [ruff](https://docs.astral.sh/ruff/) for linting and code style.

## **Setup**

1. Install development requirements:
    ```bash
    pip install -r requirements-dev.txt
    ```

2. (Optional) If your tests import Kivy modules, ensure Kivy is installed:
    ```bash
    pip install kivy
    ```

## **Running Tests**

From the `kivy_version` directory, run:
```bash
pytest
```
or to see more detailed output:
```bash
pytest -v
```

## **Linting and Code Style**

To check code style and linting with Ruff:
```bash
ruff check .
```

To automatically fix some issues:
```bash
ruff check . --fix
```

## **Best Practices**

- Write new tests for any new logic or bug fixes.
- Keep tests isolated and independent.
- Use descriptive names and thorough docstrings for all test functions.
- Run `ruff` regularly to maintain code quality and consistency.

---

See `MANUAL_TEST_PLAN.md` for manual test cases and instructions.
