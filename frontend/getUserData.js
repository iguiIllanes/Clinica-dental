const apiRequest = require("request");

function getUserData(userParameter, isDoctor){
    return new Promise(function(resolve, reject){
        
        apiRequest((isDoctor ? "http://127.0.0.1:8000/api/medicos" : "http://127.0.0.1:8000/api/pacientes") + "/" + userParameter, (err, response, body) => {
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
    getUserData: getUserData,
}