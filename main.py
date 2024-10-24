from typing import Dict, List
from autogen import ConversableAgent
from helper import extract_text_from_pdf, write_to_txt
from db_query import search_dataframe
import math
import sys
import os
import pandas as pd

def get_entrypoint_agent_system_message() -> str:
    message = "You are a helpful AI agent who will be the leader of a framework that reads a user's resume, find the 10 best"
    "jobs for that resume in the jobs dataset, and write personalized cover letters for each listing and store them in a file."
    "You will communicate with the other agents and instruct them to carry out tasks that will achieve the prompt." 
    "You will recommend which methods the agents should use."
    return message

def get_resume_agent_system_message() -> str:
    message = "You are responsible for parsing the resume. You will run the method that entrypoint_agent tells you to run and"
    "return the output from the method."
    return message

def get_db_agent_system_message() -> str:
    message = "You will read the contents of the resume in string format and then choose a keyword related to the strongest/most "
    "appealing part of the resume. Based on this keyword, you will choose the column (or columns) that are relevant to this"
    "keyword (if they keyword is a skill like Python, you should choose the 'skills' column) and call the db_query function "
    "and return the result)"
    return message

def get_cv_agent_system_message() -> str:
    message = "You will read the contents of a resume in string format and a number of job listings and write a personalized CV "
    "for each job."
    return message

def main(user_query: str):
    
    # Check for valid API key in .env variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "The OPENAI_API_KEY environment variable is not set or is invalid. Please check your .env file."
        )

    # example LLM config for the entrypoint agent
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": api_key}]}


    df = pd.read_csv('job_descriptions.csv')
    
    # ENTRYPOINT AGENT
    entrypoint_agent = ConversableAgent("entrypoint_agent", 
                                        system_message=get_entrypoint_agent_system_message, 
                                        llm_config=llm_config,)
                                        #is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0)
                                        #is_termination_msg=lambda msg: "good bye" in msg["content"].lower())

    entrypoint_agent.register_for_llm(name="extract_text_from_pdf", description="Parses pdf content into strings.")(extract_text_from_pdf)
    entrypoint_agent.register_for_execution(name="extract_text_from_pdf")(extract_text_from_pdf)

    entrypoint_agent.register_for_llm(name="search_dataframe", description="Given a keyword and a list of target columns, returns a certain number of rows that fit has columns that match the keyword.")(search_dataframe)
    entrypoint_agent.register_for_execution(name="search_dataframe")(search_dataframe)

    entrypoint_agent.register_for_llm(name="write_to_txt", description="Given a string, writes it to a designated file.")(write_to_txt)
    entrypoint_agent.register_for_execution(name="write_to_txt")(write_to_txt)

    # RESUME AGENT
    resume_agent_system_message = get_resume_agent_system_message 
    resume_agent = ConversableAgent("resume_agent", 
                                        system_message=resume_agent_system_message, 
                                        llm_config=llm_config,
                                        )
    
    resume_agent.register_for_llm(name="extract_text_from_pdf", description="Parses pdf content into strings.")(extract_text_from_pdf)
    resume_agent.register_for_execution(name="extract_text_from_pdf")(extract_text_from_pdf)

    # DATABASE AGENT
    db_agent_system_message = get_db_agent_system_message
    db_agent = ConversableAgent("db_agent", 
                                        system_message=db_agent_system_message, 
                                        llm_config=llm_config,
                                        )
    db_agent.register_for_llm(name="search_dataframe", description="Given a keyword and a list of target columns, returns a certain number of rows that fit has columns that match the keyword.")(search_dataframe)
    db_agent.register_for_execution(name="search_dataframe")(search_dataframe)

    # CV AGENT
    cv_agent_system_message = get_cv_agent_system_message
    cv_agent = ConversableAgent("cv_agent", 
                                        system_message=cv_agent_system_message, 
                                        llm_config=llm_config,
                                        )
    
    cv_agent.register_for_llm(name="write_to_txt", description="Given a string, writes it to a designated file.")(write_to_txt)
    cv_agent.register_for_execution(name="write_to_txt")(write_to_txt)


    chat_results = entrypoint_agent.initiate_chats(
        [
            {
                "recipient": resume_agent,
                "message": "Parse this pdf: " + user_query + "Once you are finished, say TERMINATE",
                "max_turns":1,
                
                "summary_method": "last_msg",
            }
        ]
    )
    print("chat results: ")
    print(chat_results)
    function_to_call = eval(chat_results[-1].chat_history[1]['tool_calls'][0]['function']['name'])
    function_arguments = eval(chat_results[-1].chat_history[1]['tool_calls'][0]['function']['arguments'])
    function_result = function_to_call(**function_arguments)

    print(function_result)
    analysis_results = entrypoint_agent.initiate_chats(
        [
            {
                "recipient": db_agent,
                "message": f"Here is the string version of the resume: {function_result}, please find the keyword for this resume and use this to find the 10 rows from the job_descriptions dataset that would be a good fit for this resume. When choosing the columns, here are some guide lines: if the keyword is a technical skill, choose the column 'skills'. When you are finished, print the rows you have found.",
                "max_turns":2,
                "max_consecutive_auto_reply":1,
                "summary_method": "last_msg",
            },
            {
                "recipient": cv_agent,
                "message": f"Here is the string version of the resume: {function_result}, use the list of jobs from the end of the previous conversation to create personalized cover letters for each job. Remeber you can use any information on the resume that will convey the user's qualifications for the specific job listing (not just the keyword, although it will likely be helpful). Once you are done, store the letters together in a file using the write_to_text function. Remember to call this function once with all of the letters together as the input.",
                "max_turns":2,
                "max_consecutive_auto_reply":1,
                "summary_method": "last_msg",
            }
        ]
    )

if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query for some restaurant when executing main."
    main(sys.argv[1])