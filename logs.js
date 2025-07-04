import express from 'express'
import bodyParser from 'body-parser'
import fetch from 'node-fetch'

const app = express()
app.use(bodyParser.json())

// this handles the log request from flask
app.post('/log', async (req, res) => {
    const { stack, level, packageName, message } = req.body

    // creds for token, no auth for real user required
    const authData = {
        companyName: "medical",
        clientID: "dummyclientid",
        clientSecret: "dummyclientsecret",
        ownerEmail: "youremail@example.com"
    }

    try {
        // get token first from test auth API
        const auth = await fetch("http://20.244.56.144/test/auth", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(authData)
        })

        const tokenData = await auth.json()
        const token = tokenData.access_token

        // send actual log to logging API (protected route)
        await fetch("http://20.244.56.144/evaluation-service/logs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
                stack: stack.toLowerCase(),  // assuming backend/frontend
                level: level.toLowerCase(),  // like error/info
                package: packageName.toLowerCase(),
                message: message
            })
        })

        // not sending back real response here
        res.send({ success: true })
    } catch (err) {
        // error in logging, not app crash
        console.log("log failed, maybe auth or API issue")
        res.status(500).send({ error: "log error" })
    }
})

// basic logger runs on 4000
app.listen(4000, () => {
    console.log("Logger up on port 4000")
})