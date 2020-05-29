from test_search import Search
from search_index import Search as S
import time
import json
def main():

    while True:
        query = input("Search: ")
        if query == "quit()":
            break
        start = time.time()
        results = Search(query)
        pages = results.new_getPages()
        end = time.time()
        # this runs only when everything runs fine
        if pages:
            print("\nHere are the top 5 relevant websites!")
            with open("docID_url.json", "r") as file:
                data = json.load(file)
            for count, i in enumerate(pages):
                print(f"{count+1}: ", data[str(i[0])])
            print()
        
        print(end - start)

        













if __name__ == "__main__":
    main()