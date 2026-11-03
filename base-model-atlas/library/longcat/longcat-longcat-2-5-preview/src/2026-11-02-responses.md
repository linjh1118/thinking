Responses API | LongCat API Docs
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
Responses API
Copy
Create a model response using the
OpenAI Responses-compatible format
. Supports multi-turn conversations, multimodal input, structured output, and tool calling, with both streaming (
stream:true
, SSE) and non-streaming responses.
POST
https://api.longcat.chat/openai/v1/responses
Authorizations
Authorization
string
header
required
Authentication key, passed in the request header as
Bearer YOUR_API_KEY
.
Body
application/json
model
string
required
Model identifier. Currently supports
LongCat-2.5
.
input
string | array
required
The input content, in two forms:
String: equivalent to a single
user
message, e.g.
"input": "Hello"
.
Message/item array: for multi-turn conversations, multimodal input, and tool result backfill. Array elements can be:
Message items:
{ "role": "user" | "assistant" | "system" | "developer", "content": ... }
, where
content
is a string or an array of content parts (e.g.
input_text
,
input_image
).
Tool result items:
{ "type": "function_call_output", "call_id": "...", "output": "..." }
.
Note: image URLs must be publicly accessible.
instructions
string
optional
System/developer instructions.
stream
boolean
optional
default: false
Whether to return the response as an SSE stream. When the stream ends normally, the connection is closed directly without an extra
[DONE]
marker.
tools
array
optional
Tools the model may call while generating the response. Tool fields (
type
,
name
, etc.) are declared
flat
on the tool object — do NOT wrap them in a
function
sub-object (that is the Chat Completions shape; this API rejects it with
tools[0].name is required
). See the "Function Calling" and "Custom Tools" scenarios on the right.
Hide child attributes
Define a function in your own code that the model may choose to call.
tools.type
string
required
Tool type, fixed to
function
.
tools.name
string
required
The function name.
tools.description
string
optional
Function description, used by the model to decide when to call it.
tools.parameters
object
required
Function parameters, described as a JSON Schema object.
tools.strict
boolean
optional
default: false
Whether to strictly enforce the parameter schema when generating function calls.
A custom tool with free-text or grammar-constrained output.
tools.type
string
required
Tool type, fixed to
custom
.
tools.name
string
required
The tool name.
tools.description
string
optional
Description of what the tool does.
tools.format
object
optional
Output format constraint:
{ "type": "text" }
for free text, or
{ "type": "grammar", "syntax": "lark" | "regex", "definition": "<grammar or regex>" }
for grammar-constrained output.
parallel_tool_calls
boolean
optional
default: true
Whether the model may call multiple tools in parallel.
temperature
number
optional
default: 1.0
Sampling temperature. Fixed at
1.0
with thinking enabled and
0.7
with thinking disabled; other values are overridden with the corresponding default.
top_p
number
optional
default: 0.95
Nucleus sampling parameter, range
(0, 1]
. For example,
0.1
means the model only considers tokens comprising the top 10% of probability mass.
max_output_tokens
integer
optional
Maximum number of tokens the model may generate (including reasoning tokens).
reasoning
object
optional
Reasoning controls.
effort
:
none
/
minimal
/
low
/
medium
/
high
/
xhigh
;
summary
:
auto
/
concise
/
detailed
.
text
object
optional
Configure the format of the text response.
format.type
values:
text
(plain text, default),
json_object
(guarantees valid JSON without field validation),
json_schema
(strictly constrains fields and types by a schema; requires
name
and
schema
). See the "Structured Output" scenario on the right for a full example.
For both JSON modes, we recommend explicitly asking the model to "answer in JSON" in
input
/
instructions
.
metadata
object
optional
String key-value metadata, returned with the response object.
prompt_cache_key
string
optional
Prompt cache key.
Response Object
On success, an object with
object:"response"
is returned; fields with
null
values are omitted:
id
string
ID of this response (
resp_xxx
).
object
string
Object type, always
response
.
status
string
Response status:
completed
(finished),
failed
(run failed, see
error
),
incomplete
(truncated, e.g.
max_output_tokens
reached).
output
array
Array of output items for this response (length and order depend on the model's actual calls). Assistant text lives in
content[].text
of the
message
item.
Hide child attributes
output.message
object
Assistant message item:
{ "id": "msg_xxx", "role": "assistant", "content": [{ "type": "output_text", "text": "...", "annotations": [] }] }
.
output.reasoning
object
Reasoning item, containing the model's chain-of-thought content.
output.function_call
object
Function call item; the client must execute the function and backfill
function_call_output
:
{ "call_id": "call_xxx", "name": "get_weather", "arguments": "{\"city\":\"Beijing\"}" }
.
output.custom_tool_call
object
Custom tool call item.
usage
object
Token usage statistics.
Hide child attributes
usage.input_tokens
integer
Number of input tokens;
input_tokens_details.cached_tokens
is the portion served from cache.
usage.output_tokens
integer
Number of output tokens;
output_tokens_details.reasoning_tokens
is the portion used for reasoning.
usage.total_tokens
integer
Total number of tokens.
error
object
Error details
{ "code", "message" }
when the run failed; omitted on success.
created_at
integer
Creation time as a Unix timestamp in seconds.
completed_at
integer
Completion time as a Unix timestamp in seconds; only present on success.
The remaining fields mostly echo the request parameters:
model
,
text
,
reasoning
,
temperature
,
top_p
,
max_output_tokens
,
metadata
,
parallel_tool_calls
, etc.
Stream Events
You usually only need to handle three event types:
response.created
(start),
response.output_text.delta
(text increments), and
response.completed
(end). Every event's
data
contains
type
and
sequence_number
; lifecycle events carry the full response object in
data
.
Full event types:
Event
Description
response.created
First event; the response has been created with status
in_progress
response.in_progress
The response is being generated
response.output_item.added
response.output_item.done
An output item (
reasoning
/
message
/
function_call
/
custom_tool_call
) started / finished
response.content_part.added
response.content_part.done
A content part within an output item started / finished
response.reasoning_text.delta
response.reasoning_text.done
Reasoning text increment / complete reasoning text
response.output_text.delta
response.output_text.done
Output text increment / complete output text
response.function_call_arguments.delta
response.function_call_arguments.done
Function call arguments increment / complete arguments
response.custom_tool_call_input.delta
response.custom_tool_call_input.done
Custom tool call input increment / complete input
response.completed
Final event on success; carries the full response object including
usage
response.incomplete
Final event when the response is truncated (e.g.
max_output_tokens
reached); carries the full response object
response.failed
Final event on failure; carries the full response object with
error
details
Request Examples
cURL
Basic
bash
curl
--location
--request
POST
'https://api.longcat.chat/openai/v1/responses'
\
--header
"Authorization: Bearer
$LONGCAT_API_KEY
"
\
--header
"Content-Type: application/json"
\
--data-raw
'{
"model": "LongCat-2.5",
"instructions": "You are a helpful assistant",
"input": "Introduce yourself in one sentence",
"temperature": 0.7,
"top_p": 0.9,
"max_output_tokens": 1024
}'
Response Examples
Non-streaming
json
{
"id"
:
"resp_311fadee0674465083b0124d0ce6408b"
,
"object"
:
"response"
,
"created_at"
:
1791623622
,
"status"
:
"completed"
,
"background"
:
false
,
"completed_at"
:
1791623627
,
"model"
:
"LongCat-2.5"
,
"output"
: [
{
"type"
:
"reasoning"
,
"id"
:
"rs_resp_311fadee0674465083b0124d0ce6408b"
,
"summary"
: [],
"content"
: [
{
"type"
:
"reasoning_text"
,
"text"
:
"The user is greeting me; I should respond warmly and introduce myself."
}
]
},
{
"type"
:
"message"
,
"id"
:
"msg_ee0f6ae4902443ac80cfdefd6e2f0230"
,
"status"
:
"completed"
,
"role"
:
"assistant"
,
"content"
: [
{
"type"
:
"output_text"
,
"text"
:
"Hello! I am LongCat, an AI assistant that can answer questions, provide information, and help with various tasks."
,
"annotations"
: []
}
]
}
],
"parallel_tool_calls"
:
true
,
"reasoning"
: {
"effort"
:
null
,
"summary"
:
null
},
"service_tier"
:
"default"
,
"store"
:
true
,
"text"
: {
"format"
: {
"type"
:
"text"
},
"verbosity"
:
"medium"
},
"tool_choice"
:
"auto"
,
"tools"
: [],
"truncation"
:
"disabled"
,
"usage"
: {
"input_tokens"
:
14
,
"input_tokens_details"
: {
"cached_tokens"
:
0
},
"output_tokens"
:
26
,
"output_tokens_details"
: {
"reasoning_tokens"
:
16
},
"total_tokens"
:
40
},
"metadata"
: {}
}
Previous
Chat Completions
Next
Anthropic Messages