import pandas as pd

# Load the dataset


def search_dataframe(columns: list[str], keyword: str, limit: int = 10) -> str:
    """
    Search the DataFrame based on a keyword in specified columns.

    :param df: Pandas DataFrame to search
    :param columns: List of column names to search for the keyword
    :param keyword: Keyword to search for
    :param limit: Number of rows to return
    :return: Filtered DataFrame
    """
    # Ensure the keyword is a string
    df = pd.read_csv('job_descriptions.csv')
    
    keyword = str(keyword)

    # Initialize a mask to filter rows
    mask = pd.Series([False] * len(df))

    # Iterate over the specified columns
    for column in columns:
        if column in df.columns:
            # Create a mask for each column where the keyword is found
            mask |= df[column].str.contains(keyword, case=False, na=False)

    # Filter the DataFrame using the mask
    filtered_df = df[mask]

    # Return the specified number of rows
    return filtered_df.head(limit).to_json(orient='records')

# # Example usage
# columns_to_search = ['Job Description', "skills"]   # Replace with your column names
# keyword = 'HTML'  # Replace with the keyword you want to search for

# results = search_dataframe(columns=columns_to_search, keyword=keyword, limit=10)
# #results = search_dataframe(columns=["Experience","Company"],keyword="Python",limit=10)
# # # Display the results
# print(results)
