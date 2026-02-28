from dispatcher import TaskDispatcher
from sources import FileSource, GeneratorSource, APISource

def main():
    sources = [
        FileSource("src/data/data.json"),
        GeneratorSource(5),
        APISource()
    ]
    dispatcher = TaskDispatcher(sources)
    dispatcher.process_all()

if __name__ == "__main__":
    main()
