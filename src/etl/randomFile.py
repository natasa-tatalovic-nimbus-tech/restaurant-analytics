import os


def main():
    files = os.listdir("sql/create")
    # Extracts the number before the first underscore and converts to int
    sorted_files = sorted(files, key=lambda x: int(x.split("_")[0]))
    print(sorted_files)


if __name__ == "__main__":
    main()
