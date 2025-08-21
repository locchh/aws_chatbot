# aws_chatbot
AWS chatbot

# guide

test `/answer`:

```
curl -X POST "http://localhost:8000/answer" \
-H "Content-Type: application/json" \
-d '{"prompt": "question: Who has control of the data security in an AWS account?\nAWS Security Team\nAWS Account Owner\nAWS Technical\nAccount Manager (TAM)\nAWS Support Team", "max_tokens": 50}'
```
# shout out to

[aws_cloud](https://chlocdev.github.io/aws_cloud/index.html)
