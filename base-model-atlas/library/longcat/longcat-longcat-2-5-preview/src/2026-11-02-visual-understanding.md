Visual Understanding | LongCat API Docs
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
Copy
Visual Understanding
​
The LongCat-2.5 model accepts images and videos alongside text. You can ask the model to describe an image, read text from a screenshot, analyze a chart, or understand video content.
Passing Images
​
There are two ways to provide images. Both use the standard OpenAI-compatible chat completions format, where
content
is an array of blocks rather than a plain string.
Method 1: Base64-Encoded Image (Inline)
​
Encode the image and embed it directly in the request as a
data:
URL — the simplest option for local files. Base64 data counts toward the request body size limit (see
Limits
).
python
import
base64
from
openai
import
OpenAI
client
=
OpenAI(
api_key
=
"YOUR_API_KEY"
,
base_url
=
"https://api.longcat.chat/openai"
)
with
open
(
"image.jpg"
,
"rb"
)
as
f:
b64
=
base64.b64encode(f.read()).decode(
"utf-8"
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
: [
{
"type"
:
"text"
,
"text"
:
"What is in this image?"
},
{
"type"
:
"image_url"
,
"image_url"
: {
"url"
:
f
"data:image/jpeg;base64,
{
b64
}
"
},
},
],
}
],
)
print
(response.choices[
0
].message.content)
bash
curl
https://api.longcat.chat/openai/v1/chat/completions
\
-H
"Content-Type: application/json"
\
-H
"Authorization: Bearer YOUR_API_KEY"
\
-d
'{
"model": "LongCat-2.5",
"messages": [
{
"role": "user",
"content": [
{"type": "text", "text": "What is in this image?"},
{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,<BASE64_DATA>"}}
]
}
]
}'
Method 2: External Image URL
​
Pass a publicly accessible
http(s)
link, and the model downloads the image automatically.
python
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
: [
{
"type"
:
"text"
,
"text"
:
"Describe this image."
},
{
"type"
:
"image_url"
,
"image_url"
: {
"url"
:
"https://example.com/image.jpg"
},
},
],
}
],
)
print
(response.choices[
0
].message.content)
Passing Videos
​
Videos can only be provided via URL — the model downloads and parses the video content automatically. It uses the same content block array format, with the video carried in a
video_url
block:
python
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
: [
{
"type"
:
"text"
,
"text"
:
"What happens in this video?"
},
{
"type"
:
"video_url"
,
"video_url"
: {
"url"
:
"https://example.com/video.mp4"
},
},
],
}
],
)
print
(response.choices[
0
].message.content)
Limits
​
Image Limits
​
Item
Value
Supported formats
PNG, JPG, JPEG, WebP, GIF (SVG, HEIC/HEIF not supported)
Input methods
Base64 encoding, URL
Original aspect ratio
Over 200:1 returns an error
Max size per image
10 MB
Max images per request
100
Video Limits
​
Item
Value
Max size per video
100 MB
Max videos per request
10
Max duration per video
Less than 3600 seconds
API Information
​
OpenAI-Compatible API
​
Image understanding uses the standard OpenAI-compatible chat completions endpoint:
Request path:
POST https://api.longcat.chat/openai/v1/chat/completions
Model name:
LongCat-2.5
Image content block:
{"type": "image_url", "image_url": {"url": "..."}}
— url accepts a public URL or a
data:
URL (Base64)
Video content block:
{"type": "video_url", "video_url": {"url": "..."}}
— url accepts public URLs only
Anthropic-Compatible API
​
Besides the OpenAI-compatible endpoint, images can also be passed via the Anthropic-compatible
/messages
endpoint (base_url:
https://api.longcat.chat/anthropic
). The difference lies in the image content block structure: Anthropic uses an
image
block whose
source
object has a
type
of either
base64
or
url
:
python
import
anthropic
client
=
anthropic.Anthropic(
api_key
=
"YOUR_API_KEY"
,
base_url
=
"https://api.longcat.chat/anthropic"
)
message
=
client.messages.create(
model
=
"LongCat-2.5"
,
max_tokens
=
1024
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
: [
{
"type"
:
"text"
,
"text"
:
"What is in this image?"
},
{
"type"
:
"image"
,
"source"
: {
"type"
:
"base64"
,
"media_type"
:
"image/jpeg"
,
"data"
:
"<BASE64_DATA>"
,
},
},
],
}
],
)
print
(message.content)
Previous
API Overview
Next
Chat Completions
On this page
Passing Images
Method 1: Base64-Encoded Image (Inline)
Method 2: External Image URL
Passing Videos
Limits
Image Limits
Video Limits
API Information
OpenAI-Compatible API
Anthropic-Compatible API