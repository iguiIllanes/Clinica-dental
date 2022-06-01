const apiRequest = require("request");

function getFichas(id_doctor, id_paciente){
    if(typeof id_doctor == 'undefined'){
        return "";
    }
    return new Promise(function(resolve, reject){
        apiRequest("http://127.0.0.1:8000/api/citas/paciente/" + id_doctor + "/" + id_paciente, (err, response, body) => {
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
    getFichas: getFichas
}