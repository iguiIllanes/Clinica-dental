const apiRequest = require("request");

function getMedicos(){
    return new Promise(function(resolve, reject){
        apiRequest("http://127.0.0.1:8000/api/medicos", (err, response, body) => {
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
    getMedicos: getMedicos
}