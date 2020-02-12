const express = require('express');
const gauth = require('./gauth');
const jssha = require("./lib/jssha-1.31.min");
//const jsSHA = require('jssha');
const app = express();

const bodyParser = require('body-parser');

const keyUtilities = new gauth.KeyUtilities(jssha.jsSHA);
//const keyUtilities = new gauth.KeyUtilities(jsSHA);

const port = 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.get('/key', (req, res) =>
{
    var secret = req.query.secret;    
    if(secret != undefined)
    {
        secret = secret.replace(/ /g, '');
        var key = keyUtilities.generate(secret);
        return res.send({"key": key});
    }   
    else
    {
        return res.send({"key": null});
    }
});

app.listen(port, () => 
{
    console.log("Server listen on port " + port);
});