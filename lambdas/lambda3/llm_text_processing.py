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
    input = body.get("text", "")
    system_prompts = body.get("prompt", "")
    temparature = body.get("temparature", 0)
    logger.info("Text: " + input)
    logger.info("Prompt: " + system_prompts)
    # create prompt template
    template = "Prompt that was provided is: {system_prompts}.Text that was provided is: {input}."
    prompt = PromptTemplate(
        input_variables=["input", "system_prompts"],
        template=template,
    )
    llm = OpenAI(temperature=temparature)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    answer = llm_chain.predict(
        text=input,
        provided_prompt=system_prompts,
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
