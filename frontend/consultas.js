const apiRequest = require("request");

function getConsultas(id_paciente){
    return new Promise(function(resolve, reject){
        apiRequest("http://127.0.0.1:8000/api/consultas/paciente/"+id_paciente, (err, response, body) => { //TODO corregir para que haga GET en base a los pacientes
            if (!err && response.statusCode == 200) {
                medicos = JSON.parse(body); // asignamos el JSON a pacientes
                resolve(medicos);
            } else {
                if(err == null){
                    resolve("");
                }else{
                    console.log("algo mas aparte del error ha pasado :O");
                }
            }
        });
    });
}  

module.exports = {
    getConsultas: getConsultas
}