const apiRequest = require("request");

function getPacientes(){
    return new Promise(function(resolve, reject){
        apiRequest("http://127.0.0.1:8000/api/pacientes", (err, response, body) => {
            if (!err && response.statusCode == 200) {
                pacientes = JSON.parse(body); // asignamos el JSON a pacientes
                resolve(pacientes);
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
    getPacientes: getPacientes
}