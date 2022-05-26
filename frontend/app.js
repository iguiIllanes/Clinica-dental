// load the things we need
var express = require('express');
var app = express();

// set the view engine to ejs
app.set('view engine', 'ejs');

// para los estilos
app.use(express.static('public'));

// index page
app.get('/', function(req, res) {
    res.render('index');
});

// inciar sesion paciente
app.get('/pacienteiniciarsesion', function(req, res){
    res.render('sign-in-paciente');
});

app.post('/iniciosesionpaciente', function(req, res){
    //TODO ver esta huevada >:v
});


app.get('/medicoiniciarsesion', function(req, res){
    res.render('sign-in-doctor');
});

// about page
app.get('/about', function(req, res) {
    res.render('pages/about');
});

app.listen(8080);
console.log('8080 is the magic port');