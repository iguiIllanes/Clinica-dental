const apiRequest = require("request");

function getPacientes(){
    return new Promise(function(resolve, reject){
        apiRequest("http://127.0.0.1:8000/api/pacientes", (err, response, body) => {
            if (!err && response.statusCode == 200) {
                pacientes = JSON.parse(body); // asignamos el JSON a pacientes
                pacientes.sort(GetSortOrder("apellido"));
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

function GetSortOrder(campo) {    
    return function(a, b) {    
        if (a['id_persona'][campo]> b['id_persona'][campo]) {    
            return 1;    
        } else if (a['id_persona'][campo]< b['id_persona'][campo]) {    
            return -1;    
        }    
        return 0;    
    }    
}    

module.exports = {
    getPacientes: getPacientes
}