// load the things we need
var express = require('express');

//configuracion para el body-parser
var bodyParser = require('body-parser');

//configuracion de express-session
var session = require('express-session');
const res = require('express/lib/response');
const { request } = require('express');

const apiRequest = require("request");

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
    options: {
        encrypt: true,
        database: "clinica-dental"
    },
    authentication:{
        type: 'default',
        options: {
            userName: 'SA',
            password: 'mssqlserver@L3v14th4nX-5y5t3m4dm1n15tr4t0r',
        }
    }
};

var connection = new Connection(config);
var Request = require('tedious').Request;

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

app.get('/', function(req, res) {
    if(req.session.loggedIn) { // para verificar si se inicio sesion
        if(req.sesion.isDoctor){ // para verificar si es doctor //TODO VER LA VARIABLE DE sesion de doctor en login doctor
            res.redirect('/doctor-panel-de-control');
        }else{
            res.redirect('/paciente-panel-de-control');
        }
    }else{
        res.redirect('/paciente-iniciar-sesion');
    }
});

// panel de control paciente
app.get('/paciente-panel-de-control', function(req, res) {
    // aqui empezamos con el consumo de la api en /api/pacientes/
    apiRequest("http://127.0.0.1:8000/api/pacientes/"+req.session.username, (err, response, body) => {
        if(!err){
            const usuario = JSON.parse(body); // asignamos el JSON a paciente
            const nombre = usuario.id_persona.nombre; // accedemos al contenido de paciente
            const apellido = usuario.id_persona.apellido;

            res.render('paciente-menu',{ // pasamos los datos de paciente a paciente-menu
                nombre: nombre,
                apellido: apellido,
            });
        }else{
            res.send("Algo ocurrio con la conexion al API. Intenta mas tarde.")
        }
    })
});

app.get('/doctor-panel-de-control', function(req,res){
    // aqui empezamos con el consumo de la api en /api/pacientes/
    apiRequest("http://127.0.0.1:8000/api/medicos/"+req.session.username, (err, response, body) => {
        if(!err){
            const usuario = JSON.parse(body); // asignamos el JSON a paciente
            const nombre = usuario.id_persona.nombre; // accedemos al contenido de paciente
            const apellido = usuario.id_persona.apellido;

            res.render('paciente-menu',{ // pasamos los datos de paciente a paciente-menu
                nombre: "Dr. "+nombre,
                apellido: apellido,
            });
        }else{
            res.send("Algo ocurrio con la conexion al API. Intenta mas tarde.")
        }
    })
});

// inciar sesion paciente
app.get('/paciente-iniciar-sesion', function(req, res){
    req.session.isDoctor = false; // para la autenticacion
    res.render('sign-in-paciente');
});

//iniciar sesion doctor
app.get('/doctor-iniciar-sesion', function(req, res){
    req.session.isDoctor = true; // para la autenticacion
    res.render('sign-in-doctor');
});

app.post('/auth', async (req, res) => { // para iniciar sesion
    username  = req.body.username
    password = req.body.password

    const query = "SELECT usuario, password FROM "+ (req.session.isDoctor ? "api_medico" : "api_paciente") + " WHERE usuario = '" + username + "' AND password = '" + password + "'";

    sqlRequest = new Request(query, function(err, rowCount){
        if(err){ // si falla algo
            res.send("Algo paso. Porfavor intenta mas tarde.")
        }else if(rowCount <= 0){ // si el registro con esos datos no existe
            res.send("Usuario y/o password incorrectos. Intenta de nuevo.")
        }else if(rowCount > 0){ // si el query es correcto
            req.session.loggedIn = true;
            req.session.username = username;
            res.redirect(req.session.isDoctor ? '/doctor-panel-de-control' : '/paciente-panel-de-control');
        }
    });

    connection.execSql(sqlRequest);
})

app.get('/info-doctores', function(req, res){
    res.render('doctors');
});


app.get('/historial-paciente', function(req, res){
    res.render('patient-profile');
});

app.get('/agendarcita', function(req, res){
    res.render('book-appointment');
});


app.get('/anadirpago', function(req, res){
    res.render('add-payments');
});


app.get('/medicoiniciarsesion', function(req, res){
    res.render('sign-in-doctor');
});

app.get('/pagos-paciente', function(req, res){
    res.render('patient-invoice');
});


app.get('/agenda-doctor', function(req, res){
    res.render('doctor-schedule');
});


app.get('/pagos', function(req, res){
    res.render('payments');
});


app.get('/anadir-doctor', function(req, res){
    res.render('add-doctor');
});

app.get('/perfil-doctor', function(req, res){
    res.render('profile');
});

// about page
app.get('/about', function(req, res) {
    res.render('pages/about');
});

app.listen(8080);
console.log('8080 is the magic port');
