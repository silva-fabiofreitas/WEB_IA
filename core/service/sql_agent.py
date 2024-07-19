        # from django.conf import settings
        # from langchain_community.utilities import SQLDatabase
        # from langchain_openai import ChatOpenAI
        # from langchain.chains import create_sql_query_chain

        # from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

        # from operator import itemgetter

        # from langchain_core.output_parsers import StrOutputParser
        # from langchain_core.prompts import PromptTemplate
        # from langchain_core.runnables import RunnablePassthrough

        # answer_prompt = PromptTemplate.from_template(
        #     """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

        # Question: {question}
        # SQL Query: {query}
        # SQL Result: {result}
        # Answer: """
        # )

        # llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

        # db_settings = settings.DATABASES["default"]
        # db_engine = db_settings["ENGINE"]
        # db_name = db_settings["NAME"]
        # db_user = db_settings["USER"]
        # db_password = db_settings["PASSWORD"]
        # db_host = db_settings["HOST"]
        # db_port = db_settings["PORT"]
        # db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        # print(db_uri)

        # db = SQLDatabase.from_uri(db_uri)

        # execute_query = QuerySQLDataBaseTool(db=db)
        # write_query = create_sql_query_chain(llm, db)

        # chain = (
        #     RunnablePassthrough.assign(query=write_query).assign(
        #         result=itemgetter("query") | execute_query
        #     )
        #     | answer_prompt
        #     | llm
        #     | StrOutputParser()
        # )
        ###############
        # from langchain_community.agent_toolkits import SQLDatabaseToolkit

        # toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # tools = toolkit.get_tools()
        
        # from langchain_core.messages import SystemMessage

        # SQL_PREFIX = """You are an agent designed to interact with a SQL database.
        # Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
        # Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
        # You can order the results by a relevant column to return the most interesting examples in the database.
        # Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        # You have access to tools for interacting with the database.
        # Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        # You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        # DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        # To start you should ALWAYS look at the tables in the database to see what you can query.
        # Do NOT skip this step.
        # Then you should query the schema of the most relevant tables."""

        # system_message = SystemMessage(content=SQL_PREFIX)
        
        # from langchain_core.messages import HumanMessage
        # from langgraph.prebuilt import create_react_agent
        
        # agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)

        
        # response = chain.invoke({"question": "How many employees are there"})
        # response

        # response = StreamingHttpResponse(chain.stream({"question": question}))
        # return response
        
        # for s in agent_executor.stream(
        #     {"messages": [HumanMessage(content="10 lnhas iris")]}
        # ):
        #     print(s)
        #     print("----")
            # yield s
            
        # from langchain_community.agent_toolkits import create_sql_agent
        # from langchain_openai import ChatOpenAI

        # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        # agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
        