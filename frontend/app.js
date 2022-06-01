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
const getUserData = require("./getUserData");
const servicios = require("./servicios");
const consultas = require("./consultas");
const fichas = require("./fichas");

var app = express();


const date = new Date();
const fechaActual = date.getFullYear() + "-" + ((date.getMonth() + 1 < 10) ? "0" + (date.getMonth() + 1) : (date.getMonth() + 1)) + "-" + ((date.getDate() < 10) ? "0" + date.getDate() : date.getDate());

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

function checkSession(req, res) {
    if (!req.session.loggedIn) {
        res.redirect('/');
    }
}

app.get('/', function (req, res) { // -> paneles de control
    if (req.session.loggedIn) { // para verificar si se inicio sesion
        if (req.session.isDoctor) { // para verificar si es doctor //TODO -> DONE,creo | VER LA VARIABLE DE sesion de doctor en login doctor
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

app.post('/paciente-panel-de-control', function (req, res) {
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
        if (!error) {
            apiRequest("http://127.0.0.1:8000/api/pacientes/" + req.session.username, async (err, response, body) => {
                if (!err) {
                    const usuario = JSON.parse(body); // asignamos el JSON a paciente
                    const id_paciente = usuario.id_persona.id_persona;
                    const nombre = usuario.id_persona.nombre; // accedemos al contenido de paciente
                    const apellido = usuario.id_persona.apellido;
                    const cal = (await calendarioPaciente.getCalendario(id_paciente)) == null ? "" : await calendarioPaciente.getCalendario(id_paciente);
                    const medicosJSON = await medicos.getMedicos();
                    res.render('paciente-menu', { // pasamos los datos de paciente a paciente-menu
                        nombre: nombre,
                        apellido: apellido,
                        id_paciente: id_paciente,
                        calendario: cal,
                        medicos: medicosJSON,
                        numMedicos: medicosJSON.length,
                        fecha: fechaActual,

                        //para SweetAlerts
                        alert: true,
                        alertTitle: "Reservación",
                        alertMessage: "Reservación exitosa!",
                        alertIcon: 'info',
                        showConfirmButton: false,
                        time: 1500,
                        ruta: '' // vacio porque redirige a la ruta '/'
                    });
                } else {
                    res.send('Algo ocurrio con el API. Por favor intenta mas tarde.');
                }
            });
        } else {
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
        if (!error) {
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

                        // para Sweetalerts
                        alert: true,
                        alertTitle: "Reservación",
                        alertMessage: "Reservación exitosa!",
                        alertIcon: 'info',
                        showConfirmButton: false,
                        time: 1500,
                        ruta: '' // vacio porque redirige a la ruta '/'
                    });
                } else {
                    res.send("Algo ocurrio con la conexion al API. Intenta mas tarde.")
                }
            });
        } else {
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


app.post('/auth', (req, res) => { // para iniciar sesion
    isValidDoctor = true;

    username = req.body.username
    password = req.body.password

    const query = "SELECT id_persona_id, usuario, password" + (req.session.isDoctor ? ", contratado " : " ") + "FROM " + (req.session.isDoctor ? "api_medico" : "api_paciente") + " WHERE usuario = '" + username + "' AND password = '" + password + "'";
    sqlRequest = new Request(query, function (err, rowCount) {
        if (err) { // si falla algo
            res.send("Algo paso. Por favor intenta mas tarde.")
        } else if (rowCount <= 0) { // si el registro con esos datos no existe
            res.redirect('password-incorrecto');
        } else if (rowCount > 0 && isValidDoctor) {
            req.session.loggedIn = true;
            req.session.username = username;
            res.redirect(req.session.isDoctor ? '/doctor-panel-de-control' : '/paciente-panel-de-control');
        } else {
            res.redirect('/cuenta-removida');
        }
    });

    sqlRequest.on('row', function (columns) {
        req.session.ID_PERSONA = columns[0]['value']; // para poner el id_persona en las cookies

        if (req.session.isDoctor && !(columns[2]['value'])) {
            isValidDoctor = false;
        }
    });

    connection.execSql(sqlRequest);
});

app.get('/info-doctores', async function (req, res) { // -> doctors.ejs
    checkSession(req, res);
    medicosJSON = await medicos.getMedicos();
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('doctors', {
        nombre: await userData['id_persona']['nombre'],
        medicos: medicosJSON,
    });


});

app.get('/info-medicos', async function (req, res) { // -> doctors.ejs
    checkSession(req, res);
    medicosJSON = await medicos.getMedicos();
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('informacion-doctores', {
        nombre: await userData['id_persona']['nombre'],
        medicos: medicosJSON,
    });


});

app.get('/historial-paciente', async function (req, res) { // -> patient-profile.ejs
    checkSession(req, res);
    pacientesJSON = await pacientes.getPacientes();
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    serviciosJSON = await servicios.getServicios();
    // consultasJSON = await consultas.getConsultas();
    res.render('patient-profile', {
        nombre_usuario: userData['id_persona']['nombre'],
        nombre: "Nombre del Paciente",
        apellido: "Apellido del Paciente",
        correo: "Correo del Paciente",
        telefono: "Telefono del Paciente",
        alergias: [
            "Alergias del Paciente"
        ],
        enfermedades_base: [
            "Enfermedades base del Paciente"
        ],
        pacientes: pacientesJSON,
        fecha: fechaActual,
        servicios: serviciosJSON,
        consultas: [
            {
                "id_Cita": {
                    "id_cita":"#",
                    "fecha_consulta": "2022-05-31T01:29:00Z"
                },
                "Descripcion": "Descripcion Consulta",
                "MontoTotal": 0,
                "id_Servicio": {
                    "nombre_servicio": "Nombre de servicio"
                }
            }
        ],
        fichas: [],
    });
});

app.post('/historial-paciente', function (req, res) {

    id_persona = req.body.id_persona;
    if (id_persona.length > 0) { // 
        apiRequest("http://127.0.0.1:8000/api/pacientes/" + id_persona, async (err, response, body) => {
            if (!err) {
                const paciente = JSON.parse(body); // asignamos el JSON a paciente
                const nombre = paciente.id_persona.nombre; // accedemos al contenido de paciente
                const apellido = paciente.id_persona.apellido;
                const correo = paciente.correo_paciente;
                const telefono = paciente.id_persona.telefono;
                const alergias = paciente.alergias;
                const enfermedades_base = paciente.enfermedades_base;
                const pacientesJSON = await pacientes.getPacientes();
                const serviciosJSON = await servicios.getServicios();
                const consultasJSON = await consultas.getConsultas(id_persona); //TODO pasar parametro de usuario
                const userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
                const fichasJSON = await fichas.getFichas(req.session.ID_PERSONA, id_persona);
                res.render('patient-profile', { // pasamos los datos de paciente a paciente-menu
                    nombre_usuario: userData['id_persona']['nombre'],
                    nombre: nombre,
                    apellido: apellido,
                    correo: correo,
                    telefono: telefono,
                    alergias: alergias.split(','),
                    enfermedades_base: enfermedades_base.split(','),
                    pacientes: pacientesJSON,
                    fecha: fechaActual,
                    servicios: serviciosJSON,
                    consultas: consultasJSON,
                    fichas: fichasJSON,
                });
            } else {
                res.send("Algo ocurrio con la conexion al API. Intenta mas tarde.")
            }
        });
    } else {
        res.redirect('/historial-paciente')
    }
});

app.post('/anadir-historial', function (req, res) {
    /*
    
    id_Cita: 16
    Descripcion: Desc John Connor
    MontoTotal: 2022.5
    id_Servicio: 4
    */

    id_cita = req.body.ficha;
    desc = req.body.descripcion;
    id_servicio = req.body.id_servicio;
    monto_total = req.body.MontoTotal;

    if(id_cita=='' && desc=='' && id_servicio=='' && monto_total==''){
        res.redirect('/historial-paciente');
    }
    apiRequest.post({
        headers: {
            'content-type': 'application/x-www-form-urlencoded'
        },
        url: 'http://127.0.0.1:8000/api/consultas/',
        body: `id_Cita=${id_cita}&Descripcion=${desc}&MontoTotal=${monto_total}&id_Servicio=${id_servicio}`,
    }, function (error, response, body) {
        console.log(body);
        if (!error) {
            res.render('patient-profile', {
                nombre_usuario: userData['id_persona']['nombre'],
                nombre: "Nombre del Paciente",
                apellido: "Apellido del Paciente",
                correo: "Correo del Paciente",
                telefono: "Telefono del Paciente",
                alergias: [
                    "Alergias del Paciente"
                ],
                enfermedades_base: [
                    "Enfermedades base del Paciente"
                ],
                pacientes: pacientesJSON,
                fecha: fechaActual,
                servicios: serviciosJSON,
                consultas: [
                    {
                        "id_Cita": {
                            "id_cita":"#",
                            "fecha_consulta": "2022-05-31T01:29:00Z"
                        },
                        "Descripcion": "Descripcion Consulta",
                        "MontoTotal": 0,
                        "id_Servicio": {
                            "nombre_servicio": "Nombre de servicio"
                        }
                    }
                ],
                fichas: [],

                // para sweetalerts
                alert: true,
                alertTitle: "Registro",
                alertMessage: "Registro exitoso!",
                alertIcon: 'success',
                showConfirmButton: false,
                time: 1500,
                ruta: '' 
            });
        } else {
            res.send('Algo ocurrio. Por favor intenta mas tarde.');
        }
    });
});

app.get('/historial', async function (req, res) { // -> patient-profile.ejs
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('historial-paciente', {
        nombre: await userData['id_persona']['nombre'],
    });
});

app.get('/agendarcita', async function (req, res) { // -> book-appointment.ejs
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('book-appointment', {
        nombre: await userData['id_persona']['nombre'],
    });
});


app.get('/anadirpago', async function (req, res) { // -> add-payments.ejs
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('add-payments', {
        nombre: await userData['id_persona']['nombre'],
    });
});

app.get('/pagos-paciente', async function (req, res) { // -> patient-invoice.ejs
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('patient-invoice', {
        nombre: await userData['id_persona']['nombre'],
    });
});

app.get('/anadir-paciente', async function (req, res) { // -> add-patient.ejs
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('add-patient', {
        nombre: await userData['id_persona']['nombre'],
    });
});

app.get('/agenda-doctor', async function (req, res) { // -> doctor-schedule.ejs
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('doctor-schedule', {
        nombre: await userData['id_persona']['nombre'],
    });
});

app.get('/pagos', async function (req, res) { // -> 
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('payments', {
        nombre: await userData['id_persona']['nombre'],
    });
});


app.get('/anadir-doctor', async function (req, res) {
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('add-doctor', {
        nombre: await userData['id_persona']['nombre'],
    });
});

app.get('/perfil-doctor', async function (req, res) {
    checkSession(req, res);
    userData = await getUserData.getUserData(req.session.username, req.session.isDoctor);
    res.render('profile', {
        nombre: await userData['id_persona']['nombre'],
    });
});

app.get('/registrate', function (req, res) {
    res.render('sign-up');
});

app.post('/registrate', function (req, res) {
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

    if (!(conf_password == password)) {
        res.send("Las contraseñas no coinciden");
    } else {
        apiRequest.post({
            headers: {
                'content-type': 'application/x-www-form-urlencoded'
            },
            url: 'http://127.0.0.1:8000/api/pacientes/',
            body: `nombre=${nombre}&apellido=${apellido}&ci=${ci}&telefono=${telefono}&fecha_nacimiento=${fecha_nacimiento}&correo_paciente=${correo_paciente}&enfermedades_base=${enfermedades_base}&alergias=${alergias}&usuario=${usuario}&password=${password}`,
        }, function (error, response, body) {
            if (!error) {
                res.render('sign-up', {
                    alert: true,
                    alertTitle: "Registro",
                    alertMessage: "Registro exitoso!",
                    alertIcon: 'success',
                    showConfirmButton: false,
                    time: 1500,
                    ruta: '' // vacio porque redirige a la ruta '/'
                });
            } else {
                res.send('Algo ocurrio. Por favor intenta mas tarde.');
            }
        });
    }


});

app.get('/password-incorrecto', function (req, res) {
    // checkSession(req, res); // hay que quitar esto o ver una forma de que funcione sin esto
    res.render('404');
});

app.get('/cuenta-removida', function (req, res) {
    checkSession(req, res);
    res.render('cuenta-removida');
});

// para cerrar sesion
app.get('/cerrar-sesion', function (req, res) {
    req.session.destroy();
    res.redirect('/');
});

app.listen(8080);
console.log('8080 is the magic port');
