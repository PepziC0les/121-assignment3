from search_index import Search


def main():
    with open("final_index.json", "r") as file:
           data = file.read() #Keep items in scope
           
    while True:
        query = input("Search: ")
        if query == "quit()":
            break
        results = Search(query, data)
        print(results)
        













if __name__ == "__main__":
    main()