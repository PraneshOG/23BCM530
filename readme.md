# How to Run
```bash

-->Start Logger Service

cd logger-service
npm install
node log.js

--> Start Flask Shortner Service
cd / shortner-service
python app.py

This project is just a lightweight HTTP URL Shortener Microservice that has been developed using Flask (Python) and also a custom logging middleware that is built in Node.js

It shortens long URLs. Codes that are custom can be used if desired.
- When unspecified, custom expiry time defaults with support to 30 minutes.
 Links will automatically expire after the set duration that was done.
Shortcodes are used to redirect users to their original URLs. This is accomplished by the usage of shortcodes.
Basic analytics involving number of hits per shortcode are tracked
- Full custom logging is done through a Node.js middleware because console.log or print are not used
Python dictionary stores data into memory.

| For Technology | The Component |
|-------------|-------------------|
   Flask           in Python is an API Server.
   Express        uses logging for Node.js.
 | Storage |       It resides inside memory (dict) |
  Auth              logging besides token-based authorization.

Method: POST
Endpoint: `/shorturls`

Request Body:
```json
{
“url”: at “https://example.com/very/long/path”
“validity”: 10,
“shortcode”: “custom123”
}