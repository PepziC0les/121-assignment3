from search_index import Search
import time

def main():

    while True:
        query = input("Search: ")
        if query == "quit()":
            break
        results = Search(query)
        results.search_index_json()
        













if __name__ == "__main__":
    main()