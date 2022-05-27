// load the things we need
var express = require('express');

//configuracion para el body-parser
var bodyParser = require('body-parser');

//configuracion de express-session
var session = require('express-session');

var app = express();


// para la configuracion de session
app.use(session({
    secret:'secret',
    resave: true,
    saveUninitialized: true,
}));



app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());


// para la base de datos en mssql
var Connection = require('tedious').Connection;
var config = {
    server: '10.147.17.7',
    options: {},
    authentication:{
        type: 'default',
        options: {
            userName: 'SA',
            password: 'mssqlserver@L3v14th4nX-5y5t3m4dm1n15tr4t0r',
        }
    }
};

var connection = new Connection(config);

connection.on('connect', function(err){
    if(err){
        console.log('Error: ', err)
    }
    console.log('Conexion exitosa');
});

connection.connect();


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

app.get('/infodoctores', function(req, res){
    res.render('doctors');
});

app.get('/agendarcita', function(req, res){
    res.render('book-appointment');
});


app.get('/anadirpago', function(req, res){
    res.render('add-payments');
});

app.post('/signinpaciente', async (req, res) => {
    iniciarSesion(req.body.username, req.body.password);
})


app.get('/medicoiniciarsesion', function(req, res){
    res.render('sign-in-doctor');
});

app.get('/anadir-doctor', function(req, res){
    res.render('add-doctor');
});

// about page
app.get('/about', function(req, res) {
    res.render('pages/about');
});

app.listen(8080);
console.log('8080 is the magic port');


//TODO corregir esto
function iniciarSesion(username, password) {
    const query = `SELECT usuario, password FROM api_paciente WHERE usuario = ${username} AND password = ${password}`;
    request = new Request(query, (err, rowCount)=>{
        if(err){
            console.log(err);
        }else{
            console.log("Bienvenido!");
        }
    });

    request.on('row', function(columns){
        columns.forEach(column =>{
            console.log(column.value);
        });
    });

    connection.execSql(request);
}