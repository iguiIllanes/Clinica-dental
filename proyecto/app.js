const express = require('express')
const app = express()
const port = 3000

app.engine('html', require('ejs').renderFile)
app.set('view engine', 'ejs');

app.use(express.urlencoded({ extended: false }));
app.use(express.json());

const dotenv = require('dotenv');
dotenv.config({ path: './env/.env' });

app.use('/resources', express.static('public'));
app.use('/resources', express.static(__dirname + '/public'));

// app.use('/static', express.static(__dirname + '/'));

const bcryptjs = require('bcryptjs');

const session = require('express-session');
app.use(session({
  secret: 'secret',
  resave: true,
  saveUninitialized: true,
}))

//invocando module conexion
const conexion = require('./database/db');

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})


const bodyparser = require('body-parser');
app.use(bodyparser.json());
app.use(bodyparser.urlencoded({
  extended: true,
}));

const multer = require('multer');
var storage = multer.diskStorage({
  destination: (req, file, callback) => {
    callback(null, './public/images');
  },
  filename: (req, file, callback) => {
    callback(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

var upload = multer({
  storage: storage
});


const path = require('path');
const { DECIMAL } = require('mysql/lib/protocol/constants/types');
const { DEC8_BIN } = require('mysql/lib/protocol/constants/charsets');


app.post('/auth', (req, res) => {
  const username = req.body.username;
  const pass = req.body.pass;
  if (username && pass) {
    conexion.query('SELECT * FROM usuario WHERE usuario = ?', [username], async (err, result) => {
      if (result.length == 0 || !(pass == result[0].pass)) {
        res.send('Usuario o contraseña incorrectos');
      } else {
        req.session.loggedin = true;
        req.session.name = result[0].nombre;
        res.redirect('/');
      }
    });
  }
});

app.post('/anadircasa', upload.single('foto'), (req, res) => {
  if (!req.file) {
    console.log('NO file upload');
  } else {
    const id = Number(req.body.id);
    const nombre = req.body.nombre;
    const precio = Number(req.body.precio);
    const pisos = Number(req.body.pisos);
    const cuartos = Number(req.body.cuartos);
    const descripcion = req.body.descripcion;
    var imgSrc = '/resources/images/' + req.file.filename;
    const insertion = [id, pisos, cuartos, precio, descripcion, nombre, imgSrc];
    console.log(req.file.filename)
    var insertData = "INSERT INTO casa SET ?";
    conexion.query(insertData, {
      id_casa: id,
      pisos: pisos,
      cuartos: cuartos,
      precio: precio,
      descripcion: descripcion,
      nombre: nombre,
      foto: imgSrc,
    }, (err, result) => {
      if (err) throw err
      res.redirect('/');
    });
  }

});

app.get('/', (req, res) => {
  if (req.session.loggedin) {
    var q = "SELECT * FROM casa";
    conexion.query(q, (err, result) => {
      res.render('sign-in', {
        login: true,
        nombre: req.session.name,
        datos: result
      });
    });

    
  } else {
    res.render('sign-in');
  }
});


// rutas
app.get('/login', (req, res) => {
  res.render('login');
});

app.get('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/');
  });
});

app.get('/anadircasa', (req, res) => {
  res.render('anadircasa');
});