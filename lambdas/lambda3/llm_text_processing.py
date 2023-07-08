import json
import os
import boto3
import logging
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain import PromptTemplate


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    logger.info(body)
    # get text from body
    text = body.get("text", "")
    provided_prompt = body.get("prompt", "")
    logger.info("Text: " + text)
    logger.info("Prompt: " + provided_prompt)
    # create prompt template
    template = "Prompt that was provided is: {provided_prompt}.Text that was provided is: {text}."
    prompt = PromptTemplate(
        input_variables=["text", "provided_prompt"],
        template=template,
    )
    llm = OpenAI(temperature=0)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    answer = llm_chain.predict(
        text=text,
        provided_prompt=provided_prompt,
    )
    logger.info("Answer: " + answer)
    result = {
        "statusCode": 200,
        "body": json.dumps(
            {
                "answer": answer,
            }
        ),
    }
    return result
