// load the things we need
var express = require('express');

//configuracion para el body-parser
var bodyParser = require('body-parser');

//configuracion de express-session
var session = require('express-session');
const res = require('express/lib/response');
const { request } = require('express');

const apiRequest = require("request");

const calendario = require("./calendario");

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

app.get('/', function(req, res) { // -> paneles de control
    if(req.session.loggedIn) { // para verificar si se inicio sesion
        if(req.session.isDoctor){ // para verificar si es doctor //TODO VER LA VARIABLE DE sesion de doctor en login doctor
            res.redirect('/doctor-panel-de-control');
        }else{
            res.redirect('/paciente-panel-de-control');
        }
    }else{
        res.redirect('/paciente-iniciar-sesion');
    }
});

// panel de control paciente
app.get('/paciente-panel-de-control', function(req, res) { // -> paciente-menu.ejs
    if(req.session.loggedIn) { // comprueba si ya hay una sesion iniciada
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
        });
    }else{
        res.redirect('/paciente-iniciar-sesion');
    }
    // aqui empezamos con el consumo de la api en /api/pacientes/
});

app.get('/doctor-panel-de-control', function(req,res){ // -> paciente-menu.ejs
    if(req.session.loggedIn){ // comprueba si la sesion ya fue iniciada
        // aqui empezamos con el consumo de la api en /api/medicos/
        apiRequest("http://127.0.0.1:8000/api/medicos/"+req.session.username, async (err, response, body) => {
            if(!err){
                const usuario = JSON.parse(body); // asignamos el JSON a paciente
                const nombre = usuario.id_persona.nombre; // accedemos al contenido de paciente
                const apellido = usuario.id_persona.apellido;
                const id_doctor = usuario.id_persona.id_persona;
                const cal = (await calendario.getCalendario(id_doctor)) == null ? "" : await calendario.getCalendario(id_doctor);
                res.render('doctor-schedule',{ // pasamos los datos de paciente a paciente-menu
                    nombre: "Dr. "+nombre,
                    apellido: apellido,
                    id_doctor: id_doctor,
                    calendario: cal,
                });
            }else{
                res.send("Algo ocurrio con la conexion al API. Intenta mas tarde.")
            }
        })
    }else{
        res.redirect('/doctor-iniciar-sesion');
    }

});

// inciar sesion paciente
app.get('/paciente-iniciar-sesion', function(req, res){ //-> sign-in-paciente.ejs
    req.session.isDoctor = false; // para la autenticacion
    res.render('sign-in-paciente');
});

//iniciar sesion doctor
app.get('/doctor-iniciar-sesion', function(req, res){ // -> sign-in-doctor.ejs
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

app.get('/info-doctores', function(req, res){ // -> doctors.ejs
    res.render('doctors');
});


app.get('/historial-paciente', function(req, res){ // -> patient-profile.ejs
    res.render('patient-profile');
});

app.get('/agendarcita', function(req, res){ // -> book-appointment.ejs
    res.render('book-appointment');
});


app.get('/anadirpago', function(req, res){ // -> add-payments.ejs
    res.render('add-payments');
});

app.get('/pagos-paciente', function(req, res){ // -> patient-invoice.ejs
    res.render('patient-invoice');
});

app.get('/anadir-paciente', function(req, res){ // -> add-patient.ejs
    res.render('add-patient');
});

app.get('/agenda-doctor', function(req, res){ // -> doctor-schedule.ejs
    res.render('doctor-schedule');
});

app.get('/pagos', function(req, res){ // -> 
    res.render('payments');
});


app.get('/anadir-doctor', function(req, res){
    res.render('add-doctor');
});

app.get('/perfil-doctor', function(req, res){
    res.render('profile');
});

// para cerrar sesion
app.get('/cerrar-sesion', function(req, res){
    req.session.destroy();
    res.redirect('/');
});

app.listen(8080);
console.log('8080 is the magic port');
