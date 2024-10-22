# 194-196-llm
To run code, upload your resume in the root folder and run 

TODOs:
Currently the search function (can be found in db_query.py) takes in one keyword and looks for this keyword in the specified columns.
We want to support multiple keyword and allow for more complex queries overall (requiring all keywords to match, requring some to match, etc...). It looks like sqlite with FTS5 could be a decent start (I've tried implementing in db_query.ipynb but haven't been successful so far).

Once the search function is improved, the prompt for db_agent should also be improved since there will be more types of possible queries.

The agents should stop conversation at the appropriate moment but right now they seem to go too far. However, everything is working despite this so this fix is low priority.