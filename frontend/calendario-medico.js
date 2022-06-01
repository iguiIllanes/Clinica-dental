const apiRequest = require("request");

const eventColors = [
	'b-l b-2x b-greensea',
	'bg-cyan',
	'b-l b-2x b-lightred',
	'b-l b-2x b-success',
	'b-l b-2x b-primary',
	'b-l b-2x b-amethyst',
	'b-l b-2x b-drank'
];

function generarCalendario(id_doctor){
    return new Promise((resolve, reject) =>{
        apiRequest("http://127.0.0.1:8000/api/citas/medico/" + id_doctor, (err, response, body) => {
            if (!err && response.statusCode == 200) {
                citas = JSON.parse(body); // asignamos el JSON a pacientes
                citasParsed = []
                for(var i =0; i<citas.length; i++) {
                    citasParsed[i]={
                        title: citas[i]['id_paciente']['nombre'] + " " + citas[i]['id_paciente']['apellido'] + " Ficha: " + citas[i]['id_cita'],
                        start: citas[i]['fecha_consulta'],
                        className: eventColors[Math.floor(Math.random() * 7)]
                    };
                }
                resolve(JSON.stringify(citasParsed));
            } else {
                if(err == null){
                    resolve("");
                }else{
                    console.log("algo mas aparte del error ha pasado :O");
                }
            }
        });
    })

}


module.exports = {
    getCalendario: generarCalendario
};