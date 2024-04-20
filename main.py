import time
from db import Sort
from src import main, console


if __name__ == "__main__":
    S = Sort()
    with console.status(
        "[bold] DrShell Framework is starting ...", spinner="aesthetic"
    ) as status:
        S.woriteJsonFile()
        time.sleep(1)
    main()
