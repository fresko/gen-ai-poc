import openai
import streamlit as st
import os
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from sqlalchemy import insert
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import SQLAutoVectorQueryEngine
#import extra_streamlit_components as stx

#FrontEnd
st.title("Hello Space People - let's talk whit your DATA !")
st.header("AGENTE AI - PREGUNTA A TU BASE DE DATOS")  
OPENAI_API_KEY = st.text_input('OPENAI_API_KEY', type='password')        
PINECONE_API_KEY = st.text_input('PINECONE_API_KEY', type='password')

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
api_key = os.environ["PINECONE_API_KEY"]

if api_key: 

    #val = stx.stepper_bar(steps=["Ready", "Get Set", "Go"])
    #st.info("Phase #{val}")
    st.title("Start ...!")

    pc = Pinecone(api_key=api_key)
    pinecone_index = pc.Index("quickstart")

   


    #llm model apikey
    #os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
    #vector db apikey
    #os.environ["PINECONE_API_KEY"] = "PINECONE_API_KEY"
    #api_key = os.environ["PINECONE_API_KEY"]


    # define pinecone vector index
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index, namespace="wiki_cities",index_name="quickstart"
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    vector_index = VectorStoreIndex([], storage_context=storage_context)

    ##Crea el schema  con lib sqlalchemy
    from sqlalchemy import (
        create_engine,
        MetaData,
        Table,
        Column,
        String,
        Integer,
        select,
        column,
    )
    engine = create_engine("sqlite:///:memory:", future=True)
    metadata_obj = MetaData()

    # create city SQL table
    table_name = "orden_compra"
    city_stats_table = Table(
        table_name,
        metadata_obj,
        Column("orden_name", String(16), primary_key=True),
        Column("valor", Integer),
        Column("proveedor", String(16), nullable=False),
    )

    metadata_obj.create_all(engine)

    #Insertar en table 
    rows = [
        {"orden_name": "ORDC1", "valor": 5000000, "proveedor": "tienda"},
        {"orden_name": "ORDC2", "valor": 6000000, "proveedor": "exito"},
        {"orden_name": "ORDC3", "valor": 10000000, "proveedor": "mercado"},
    ]
    for row in rows:
        stmt = insert(city_stats_table).values(**row)
        with engine.begin() as connection:
            cursor = connection.execute(stmt)
        with engine.connect() as connection:
            cursor = connection.exec_driver_sql("SELECT * FROM orden_compra")
            print(cursor.fetchall())

    sql_database = SQLDatabase(engine, include_tables=["orden_compra"])
    #This is the query engine that will allow you to query your database using natural language (NL).
    sql_query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=["orden_compra"],
    )

    # Caragar data desde wiki pedia
    cities = ["Toronto", "Berlin", "Tokyo"]
    wiki_docs = WikipediaReader().load_data(pages=cities)
    # Insert documents into vector index
    # Each document has metadata of the city attached
    for city, wiki_doc in zip(cities, wiki_docs):
        nodes = Settings.node_parser.get_nodes_from_documents([wiki_doc])
        # add metadata to each node
        for node in nodes:
            node.metadata = {"title": city}
        vector_index.insert_nodes(nodes)


    #LLM OPENAI
    vector_store_info = VectorStoreInfo(
        content_info="articles about different cities",
        metadata_info=[
            MetadataInfo(
                name="title", type="str", description="The name of the city"
            ),
        ],
    )
    vector_auto_retriever = VectorIndexAutoRetriever(
        vector_index, vector_store_info=vector_store_info
    )

    retriever_query_engine = RetrieverQueryEngine.from_args(
        vector_auto_retriever, llm=OpenAI(model="gpt-3.5-turbo") #gpt-4

    )


    #Consulta en lenguaje natural
    sql_tool = QueryEngineTool.from_defaults(
        query_engine=sql_query_engine,
        description=(
            "Useful for translating a natural language query into a SQL query over"
            " a table containing: orden_compra, containing the valor/proveedor of"
            " each city"
        ),
    )
    vector_tool = QueryEngineTool.from_defaults(
        query_engine=retriever_query_engine,
        description=(
            "Useful for answering semantic questions about different orden_compra"
        ),
    )

    #Consultas 
    query_engine = SQLAutoVectorQueryEngine(
        sql_tool, vector_tool, llm=OpenAI(model="gpt-3.5-turbo") #gpt-4
    )

     
    user_question = st.text_input("Haz una pregunta a tu BD :")

    if user_question:

        response = query_engine.query(user_question)
        st.write(response) 

       #"Tell me about the arts and culture of the city with the highest"
            #" population" 

       # response = query_engine.query("Tell me about the history of Berlin")
       # print(str(response))
       # st.write(response)

        #response = query_engine.query(
        #    "Can you give me the country corresponding to each city?"
        #)
        #print(str(response))
        #st.write(response)


######
#si la db vectro no exite se debe crear 
######
#pinecone_index = pc.create_index(
#    name="quickstart",
#    dimension=1536, # Replace with your model dimensions
#    metric="euclidean", # Replace with your model metric
#    spec=ServerlessSpec(
#        cloud="aws",
#        region="us-east-1"
#    ) 
#  ) 
######
# OPTIONAL: delete all
#pinecone_index.delete(deleteAll=True)

#llama_index handles translating your natural language query into a corresponding SQL query.
#It then uses the provided SQLAlchemy engine to execute the SQL query against your database.
