import requests
from qna_support.qna_usage import get_answer



def post(payload):
    input_text = payload['input_text']
    question = payload['question']

    response = get_answer(input_text, question)

    answer = eval(response)

    return {
        "input_text": input_text,
        "question": question,
        "answer": answer['answer'],
        "answer_confidence": answer['confidence']
    }