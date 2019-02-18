# NLP API
DISCLAIMER : To run this repo you need to have a google cloud account.
### Following processes can be done using this API :
- Basic Stats of a document
- Creating a wordcloud
- Topic modelling on any text
- Topic Sentiment Analysis
- Sentiment Analysis
- Entity recogination
- POS and Syntax Tagging *
- Machine Translation
- Summarisation **
- Question-Answering **

| * Under progress
| ** Working but git isn't taking the pretrained weights so you can't directly run it
### How to run the code

- Clone the repo using
```bash
git clone https://github.com/AnsujJoshi/NLP-APIs.git
```
- Go into the diectory
- Run the main file
```python
python main.py
```
As you run this command following routes will be opened via Flask API
```
/wordcloud
/stats
/sentiment
/topics
/entity
/translation
/summary
/qna
```

By providing the appropriate JSON as query you can get the appropriate results
