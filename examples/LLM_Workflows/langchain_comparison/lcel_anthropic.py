from langchain_community.chat_models import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")
output_parser = StrOutputParser()
anthropic = ChatAnthropic(model="claude-2")
anthropic_chain = {"topic": RunnablePassthrough()} | prompt | anthropic | output_parser


if __name__ == "__main__":
    print(anthropic_chain.invoke("ice cream"))
