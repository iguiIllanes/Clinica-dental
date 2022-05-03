const mysql = require('mysql');
const connection = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_DATABASE,
    port: process.env.DB_PORT
});

connection.connect((error)=>{
    if(error){
        console.log("Error en la conexion con la BD: " + error);
        return;
    }
    console.log('Connected!');
})

module.exports = connection;
