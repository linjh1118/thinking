Quick Start | LongCat API Docs
Docs
Guide
Quick Start
Token Pack
API Pay-As-You-Go
FAQ
Change Log
API
API Overview
Visual Understanding
Chat
POST
Chat Completions
POST
Responses API
POST
Anthropic Messages
Reference
Model Parameters
Models
GET
List Models
GET
Retrieve Model
Tools
Overview of AI Tools
Claude Code
Codex
OpenCode
CatPaw
Cline
Kilo Code
Cherry Studio
Chatbox
CodeBuddy
OpenClaw
Hermes Agent
CC Switch
WorkBuddy
DeepSeek Harness
Pricing
LongCat-2.5
简体中文
API Platform ↗
Docs
Search docs
⌘K
English
English
简体中文
API Platform
Guide
API
Tools
Pricing
Quick Start
Token Pack
API Pay-As-You-Go
FAQ
Change Log
Copy
LongCat API Platform Quick Start Guide
​
Welcome to the LongCat API Platform! This document will help you get started quickly and begin using our large model services.
How to Get an API Key?
​
Register an Account
​
Visit
LongCat API Platform
Fill in the required information to complete account registration
Create Your API Key
​
After registering and logging in, go to the
API Keys
page and click “Create API Key” to manually generate a key.
Once created, you can view the following details in the list:
Name: Your custom identifier for the application
Key: The system-generated secret (Your API key is only shown once upon creation. Please copy and store it securely — if lost, you'll need to create a new one.)
Supported API Types
​
LongCat API Platform is compatible with two mainstream API formats. You can choose according to your needs:
OpenAI API Format
​
Fully compatible with the OpenAI API specification, supporting the following endpoints:
Chat Completion
:
/v1/chat/completions
Anthropic API Format
​
Compatible with the Anthropic Claude API specification, supporting the following endpoint:
Message Chat
:
/v1/messages
Endpoints
​
OpenAI Format
:
https://api.longcat.chat/openai
Anthropic Format
:
https://api.longcat.chat/anthropic
Supported Models
​
Model Name
API Format
Description
LongCat-2.5
OpenAI/Anthropic
High-performance Agentic model
Rate Limiting Rules
​
Single Request Limit
​
Maximum context length
:
LongCat-2.5: 1M token context window with a maximum output length of 256K tokens
Over-limit Handling
​
When rate limiting is triggered, the API will return HTTP status code 429. Example response:
json
{
"error"
: {
"code"
:
"rate_limit_exceeded"
,
"message"
:
"Request rate limit exceeded, please try again later"
,
"type"
:
"rate_limit_error"
,
"retry_after"
:
60
}
}
It is recommended to implement exponential backoff retry mechanism on the client side.
Quick Integration Examples
​
OpenAI API Format Example
​
Python Example
​
python
import
requests
url
=
"https://api.longcat.chat/openai/v1/chat/completions"
headers
=
{
"Authorization"
:
"Bearer YOUR_APP_KEY"
,
"Content-Type"
:
"application/json"
}
data
=
{
"model"
:
"LongCat-2.5"
,
"messages"
: [
{
"role"
:
"user"
,
"content"
:
"Hello, please introduce yourself."
}
],
"max_tokens"
:
1000
,
"temperature"
:
0.7
}
response
=
requests.post(url,
headers
=
headers,
json
=
data)
print
(response.json())
Using OpenAI SDK
​
python
from
openai
import
OpenAI
client
=
OpenAI(
api_key
=
"YOUR_APP_KEY"
,
base_url
=
"https://api.longcat.chat/openai"
)
response
=
client.chat.completions.create(
model
=
"LongCat-2.5"
,
messages
=
[
{
"role"
:
"user"
,
"content"
:
"Hello!"
}
],
max_tokens
=
1000
)
print
(response.choices[
0
].message.content)
Anthropic API Format Example
​
Using Anthropic SDK
​
python
from
anthropic
import
Anthropic
client
=
Anthropic(
api_key
=
"Authorization: Bearer YOUR_APP_KEY"
,
base_url
=
"https://api.longcat.chat/anthropic"
,
default_headers
=
{
"Content-Type"
:
"application/json"
,
"Authorization"
:
"Bearer YOUR_APP_KEY"
,
}
)
response
=
client.messages.create(
model
=
"LongCat-2.5"
,
max_tokens
=
1000
,
messages
=
[
{
"role"
:
"user"
,
"content"
:
"Hello!"
}
]
)
print
(response.content[
0
].text)
cURL Example
​
OpenAI Format
​
bash
curl
-X
POST
https://api.longcat.chat/openai/v1/chat/completions
\
-H
"Authorization: Bearer YOUR_APP_KEY"
\
-H
"Content-Type: application/json"
\
-d
'{
"model": "LongCat-2.5",
"messages": [{"role": "user", "content": "Hello!"}],
"max_tokens": 1000
}'
Anthropic Format
​
bash
curl
-X
POST
https://api.longcat.chat/anthropic/v1/messages
\
-H
"Authorization: Bearer YOUR_APP_KEY"
\
-H
"Content-Type: application/json"
\
-H
"anthropic-version: 2023-06-01"
\
-d
'{
"model": "LongCat-2.5",
"max_tokens": 1000,
"messages": [{"role": "user", "content": "Hello!"}]
}'
Important Reminders
​
Please keep your API Key safe to avoid quota theft due to leakage
Now you have learned the basics of using the LongCat API Platform. Go ahead and try it out!
Next
Token Pack
On this page
How to Get an API Key?
Register an Account
Create Your API Key
Supported API Types
OpenAI API Format
Anthropic API Format
Endpoints
Supported Models
Rate Limiting Rules
Single Request Limit
Over-limit Handling
Quick Integration Examples
OpenAI API Format Example
Anthropic API Format Example
cURL Example
Important Reminders