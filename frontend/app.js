// load the things we need
var express = require('express');

//configuracion para el body-parser
var bodyParser = require('body-parser');

//configuracion de express-session
var session = require('express-session');
const res = require('express/lib/response');
const { request } = require('express');

const apiRequest = require("request");

const calendarioMedico = require("./calendario-medico");
const calendarioPaciente = require("./calendario-paciente");

const pacientes = require("./pacientes");
const medicos = require("./medicos");

var app = express();


const date = new Date();
const fechaActual = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();

// para la configuracion de session
app.use(session({
    secret: 'secret',
    resave: true,
    saveUninitialized: true,
}));



app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());


// para la base de datos en mssql
var Connection = require('tedious').Connection;
var config = {
    server: '10.147.17.7',
    options: {
        encrypt: true,
        database: "clinica-dental"
    },
    authentication: {
        type: 'default',
        options: {
            userName: 'SA',
            password: 'mssqlserver@L3v14th4nX-5y5t3m4dm1n15tr4t0r',
        }
    }
};

var connection = new Connection(config);
var Request = require('tedious').Request;

connection.on('connect', function (err) {
    if (err) {
        console.log('Error: ', err)
    }
    console.log('Conexion exitosa');
});

connection.connect();


// set the view engine to ejs
app.set('view engine', 'ejs');

// para los estilos
app.use(express.static('public'));

app.get('/', function (req, res) { // -> paneles de control
    if (req.session.loggedIn) { // para verificar si se inicio sesion
        if (req.session.isDoctor) { // para verificar si es doctor //TODO VER LA VARIABLE DE sesion de doctor en login doctor
            res.redirect('/doctor-panel-de-control');
        } else {
            res.redirect('/paciente-panel-de-control');
        }
    } else {
        res.redirect('/paciente-iniciar-sesion');
    }
});

// panel de control paciente
app.get('/paciente-panel-de-control', function (req, res) { // -> paciente-menu.ejs
    if (req.session.loggedIn) { // comprueba si ya hay una sesion iniciada
        apiRequest("http://127.0.0.1:8000/api/pacientes/" + req.session.username, async (err, response, body) => {
            if (!err) {
                const usuario = JSON.parse(body); // asignamos el JSON a paciente
                const id_paciente = usuario.id_persona.id_persona; 
                const nombre = usuario.id_persona.nombre; // accedemos al contenido de paciente
                const apellido = usuario.id_persona.apellido;
                const cal = (await calendarioPaciente.getCalendario(id_paciente)) == null ? "" : await calendarioPaciente.getCalendario(id_paciente);
                const medicosJSON = await medicos.getMedicos();
                console.log(medicosJSON);
                res.render('paciente-menu', { // pasamos los datos de paciente a paciente-menu
                    nombre: nombre,
                    apellido: apellido,
                    id_paciente: id_paciente,
                    calendario: cal,
                    medicos: medicosJSON,
                    numMedicos: medicosJSON.length,
                    fecha: fechaActual
                });
            } else {
                res.send("Algo ocurrio con la conexion al API. Intenta mas tarde.")
            }
        });
    } else {
        res.redirect('/paciente-iniciar-sesion');
    }
    // aqui empezamos con el consumo de la api en /api/pacientes/
});

app.post('/paciente-panel-de-control', function (req, res){
    id_doctor = req.body.id_doctor;
    id_paciente = req.body.id_paciente;
    fecha_reserva = req.body.fecha_reserva;
    fecha_consulta = req.body.fecha_consulta;

    apiRequest.post({
        headers: {
            'content-type': 'application/x-www-form-urlencoded'
        },
        url: 'http://127.0.0.1:8000/api/citas/',
        body: `id_doctor=${id_doctor}&id_paciente=${id_paciente}&fecha_reserva=${fecha_reserva}&fecha_consulta=${fecha_consulta}`,
    }, function (error, response, body) {
        if(!error){
            res.redirect('/paciente-panel-de-control');
        }else{
            res.send('Algo ocurrio. Por favor intenta mas tarde.');
        }
    });
});

app.get('/doctor-panel-de-control', function (req, res) { // -> paciente-menu.ejs
    if (req.session.loggedIn) { // comprueba si la sesion ya fue iniciada
        // aqui empezamos con el consumo de la api en /api/medicos/
        apiRequest("http://127.0.0.1:8000/api/medicos/" + req.session.username, async (err, response, body) => {
            if (!err) {
                const usuario = JSON.parse(body); // asignamos el JSON a paciente
                const nombre = usuario.id_persona.nombre; // accedemos al contenido de paciente
                const apellido = usuario.id_persona.apellido;
                const id_doctor = usuario.id_persona.id_persona;
                const cal = (await calendarioMedico.getCalendario(id_doctor)) == null ? "" : await calendarioMedico.getCalendario(id_doctor);
                const pacientesJSON = await pacientes.getPacientes();
                res.render('doctor-schedule', { // pasamos los datos de paciente a paciente-menu
                    nombre: "Dr. " + nombre,
                    apellido: apellido,
                    id_doctor: id_doctor,
                    calendario: cal,
                    pacientes: pacientesJSON,
                    numPacientes: pacientesJSON.length,
                    fecha: fechaActual,
                });
            } else {
                res.send("Algo ocurrio con la conexion al API. Intenta mas tarde.")
            }
        })
    } else {
        res.redirect('/doctor-iniciar-sesion');
    }
});


app.post('/doctor-panel-de-control', function (req, res) {
    id_doctor = req.body.id_doctor;
    id_paciente = req.body.id_paciente;
    fecha_reserva = req.body.fecha_reserva;
    fecha_consulta = req.body.fecha_consulta;

    apiRequest.post({
        headers: {
            'content-type': 'application/x-www-form-urlencoded'
        },
        url: 'http://127.0.0.1:8000/api/citas/',
        body: `id_doctor=${id_doctor}&id_paciente=${id_paciente}&fecha_reserva=${fecha_reserva}&fecha_consulta=${fecha_consulta}`,
    }, function (error, response, body) {
        if(!error){
            res.redirect('/doctor-panel-de-control');
        }else{
            res.send('Algo ocurrio. Por favor intenta mas tarde.');
        }
    });
});

// inciar sesion paciente
app.get('/paciente-iniciar-sesion', function (req, res) { //-> sign-in-paciente.ejs
    req.session.isDoctor = false; // para la autenticacion
    res.render('sign-in-paciente');
});

//iniciar sesion doctor
app.get('/doctor-iniciar-sesion', function (req, res) { // -> sign-in-doctor.ejs
    req.session.isDoctor = true; // para la autenticacion
    res.render('sign-in-doctor');
});


app.post('/auth', async (req, res) => { // para iniciar sesion
    username = req.body.username
    password = req.body.password

    const query = "SELECT usuario, password FROM " + (req.session.isDoctor ? "api_medico" : "api_paciente") + " WHERE usuario = '" + username + "' AND password = '" + password + "'";

    sqlRequest = new Request(query, function (err, rowCount) {
        if (err) { // si falla algo
            res.send("Algo paso. Porfavor intenta mas tarde.")
        } else if (rowCount <= 0) { // si el registro con esos datos no existe
            res.redirect('password-incorrecto');
        } else if (rowCount > 0) { // si el query es correcto
            req.session.loggedIn = true;
            req.session.username = username;
            res.redirect(req.session.isDoctor ? '/doctor-panel-de-control' : '/paciente-panel-de-control');
        }
    });

    connection.execSql(sqlRequest);
})

app.get('/info-doctores', async function (req, res) { // -> doctors.ejs

    medicosJSON = await medicos.getMedicos();
    res.render('doctors',{
        medicos: medicosJSON,
    });
});


app.get('/info-medicos', async function (req, res) { // -> info doctores.ejs

    medicosJSON = await medicos.getMedicos();
    res.render('informacion-doctores',{
        medicos: medicosJSON,
    });
});


app.get('/historial-paciente', function (req, res) { // -> patient-profile.ejs
    res.render('patient-profile');
});

app.get('/agendarcita', function (req, res) { // -> book-appointment.ejs
    res.render('book-appointment');
});


app.get('/historial', function (req, res) { // -> historial paciente.ejs
    res.render('historial-paciente');
});


app.get('/anadirpago', function (req, res) { // -> add-payments.ejs
    res.render('add-payments');
});

app.get('/pagos-paciente', function (req, res) { // -> patient-invoice.ejs
    res.render('patient-invoice');
});

app.get('/anadir_paciente', function (req, res) { // -> add-patient.ejs
    res.render('add-patient');
});

app.get('/agenda-doctor', function (req, res) { // -> doctor-schedule.ejs
    res.render('doctor-schedule');
});

app.get('/pagos', function (req, res) { // -> 
    res.render('payments');
});


app.get('/anadir-doctor', function (req, res) {
    res.render('add-doctor');
});

app.get('/perfil-doctor', function (req, res) {
    res.render('profile');
});

app.get('/registrate', function (req, res){
    res.render('sign-up');
});


app.get('/anadir-paciente', function (req, res){
    res.render('add-patient');
});

app.post('/registrate', function (req, res){
    nombre = req.body.nombre;
    apellido = req.body.apellido;
    ci = req.body.ci;
    telefono = req.body.telefono;
    fecha_nacimiento = req.body.fecha_nacimiento;
    correo_paciente = req.body.correo_paciente;
    enfermedades_base = req.body.enfermedades_base;
    alergias = req.body.alergias;
    usuario = req.body.usuario;
    password = req.body.password;
    conf_password = req.body.conf_password;


    // console.log(nombre);
    // console.log(apellido);
    // console.log(ci);
    // console.log(telefono);
    // console.log(fecha_nacimiento);
    // console.log(correo_paciente);
    // console.log(enfermedades_base);
    // console.log(alergias);
    // console.log(usuario);
    // console.log(password);


    if(!(conf_password == password)){
        res.send("Las contraseñas no coinciden");
    }else{
        apiRequest.post({
            headers: {
                'content-type': 'application/x-www-form-urlencoded'
            },
            url: 'http://127.0.0.1:8000/api/pacientes/',
            body: `nombre=${nombre}&apellido=${apellido}&ci=${ci}&telefono=${telefono}&fecha_nacimiento=${fecha_nacimiento}&correo_paciente=${correo_paciente}&enfermedades_base=${enfermedades_base}&alergias=${alergias}&usuario=${usuario}&password=${password}`,
        }, function (error, response, body) {
            if(!error){
                res.send('Usuario creado exitosamente.');
            }else{
                res.send('Algo ocurrio. Por favor intenta mas tarde.');
            }
        });
    }


});

app.post('/anadir_paciente', function (req, res){
    nombre = req.body.nombre;
    apellido = req.body.apellido;
    ci = req.body.ci;
    telefono = req.body.telefono;
    fecha_nacimiento = req.body.fecha_nacimiento;
    correo_paciente = req.body.correo_paciente;
    enfermedades_base = req.body.enfermedades_base;
    alergias = req.body.alergias;
    usuario = req.body.usuario;
    password = req.body.password;
    conf_password = req.body.conf_password;


    // console.log(nombre);
    // console.log(apellido);
    // console.log(ci);
    // console.log(telefono);
    // console.log(fecha_nacimiento);
    // console.log(correo_paciente);
    // console.log(enfermedades_base);
    // console.log(alergias);
    // console.log(usuario);
    // console.log(password);


    if(!(conf_password == password)){
        res.send("Las contraseñas no coinciden");
    }else{
        apiRequest.post({
            headers: {
                'content-type': 'application/x-www-form-urlencoded'
            },
            url: 'http://127.0.0.1:8000/api/pacientes/',
            body: `nombre=${nombre}&apellido=${apellido}&ci=${ci}&telefono=${telefono}&fecha_nacimiento=${fecha_nacimiento}&correo_paciente=${correo_paciente}&enfermedades_base=${enfermedades_base}&alergias=${alergias}&usuario=${usuario}&password=${password}`,
        }, function (error, response, body) {
            if(!error){
                res.send('Usuario creado exitosamente.');
            }else{
                res.send('Algo ocurrio. Por favor intenta mas tarde.');
            }
        });
    }


});


app.get('/password-incorrecto', function (req, res){
    res.render('404');
});


app.get('/cuenta-removida', function (req, res){
    res.render('cuenta-removida');
});

// para cerrar sesion
app.get('/cerrar-sesion', function (req, res) {
    req.session.destroy();
    res.redirect('/');
});

app.listen(8080);
console.log('8080 is the magic port');
