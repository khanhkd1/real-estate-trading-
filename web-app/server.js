const express = require('express');
const path = require('path');
const serveStatic = require('serve-static');
const app = express();
app.use(serveStatic(path.join(__dirname + "/dist")));
if (process.env.NODE_ENV === 'production') {
    app.use(express.static('client/build'));
}
app.get('*', (request, response) => {
    response.sendFile(path.join(__dirname, 'client/build', 'index.html'));
});
const port = process.env.PORT || 8080;
app.listen(port);
console.log('server started '+ port);
