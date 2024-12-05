import json

# Load the data from the JSON file
def load_data(file_path):
    """
    The function `load_data` reads and loads JSON data from a file specified by the `file_path`
    parameter.
    
    :param file_path: The `file_path` parameter in the `load_data` function is a string that represents
    the path to the file from which data needs to be loaded. This function opens the file specified by
    the `file_path`, reads its contents, and returns the data loaded from the file using the `json.load
    :return: The function `load_data` is returning the data loaded from the file located at the
    `file_path`. The data is being loaded using the `json.load()` function.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Basic search function: searches in title, genres, and tags
def search(query, data):
    """
    The function `search` searches for a query in a list of data entries based on title and genres,
    returning matching results.
    
    :param query: The `query` parameter is the search term that the user is looking for in the data. It
    could be a string representing a title or genre that the user wants to search for
    :param data: I see that the `search` function takes a `query` and a `data` parameter. The `data`
    parameter seems to be a list of dictionaries where each dictionary represents an entry with keys
    like 'title' and 'genre'. The function searches through this data based on the query provided and
    :return: The `search` function returns a list of entries from the `data` that match the `query`
    based on the title or genres.
    """
    results = []
    query_lower = query.lower()

    # The line `for entry in data:` is iterating over each entry in the `data` list. In this context,
    # `data` is a list of dictionaries where each dictionary represents an entry with keys like
    # 'title' and 'genre'.
    for entry in data:
        title = entry.get('title', '').lower()
        genres = entry.get('genre', [])
        genres_lower = [x.lower() for x in genres] if isinstance(genres, list) else [genres.lower()]

        if query_lower in title or query_lower in genres_lower:
            results.append(entry)

    return results

# Display the search results
def display_results(results):
    """
    The function `display_results` takes a list of results and prints out specific information about
    each result, or a message if no results are found.
    
    :param results: The `display_results` function takes a list of dictionaries as input, where each
    dictionary represents a result with keys like 'title', 'genre', 'companies', 'repack_size', and
    'original_size'. The function then iterates over the list and prints out the details of each result
    in a
    """
    # The `if results:` statement is checking if the `results` list is not empty. If there are results
    # found from the search operation, the condition `if results:` will evaluate to `True`, and the
    # code block under this `if` statement will be executed. In this case, the code block iterates
    # over the results and displays specific information about each result using the `display_results`
    # function.
    if results:
        for i, result in enumerate(results):
            print(f"Result {i + 1}:")
            print(f"Title: {result.get('title')}")
            print(f"Genres/Tags: {result.get('genre')}")
            print(f"Company: {result.get('companies')}")
            print(f"Repack Size: {result.get('repack_size')}")
            print(f"Original Size: {result.get('original_size')}")
            print("-------------")
    else:
        print("No results found.")

# Main function to drive the search engine
def main():
    """
    The main function loads data from a JSON file, prompts the user for a search query, searches the
    data based on the query, and displays the results.
    """
    # Load data from JSON file
    file_path = 'data.json'
    data = load_data(file_path)

    # Prompt user for a search query
    query = input("Enter search term: ")

    # Search the data
    results = search(query, data)

    # Show the results
    display_results(results)

if __name__ == '__main__':
    main()
