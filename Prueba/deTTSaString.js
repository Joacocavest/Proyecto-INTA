let msjTTS = '"{"end_device_ids":{"device_id":"eui-70b3d57ed0066872","application_ids":{"application_id":"nodogiiot-1"},"dev_eui":"70B3D57ED0066872","dev_addr":"260D0A4C"},"correlation_ids":["gs:uplink:01HZ28Z3AT9SJQF8N24AMNV45X"],"received_at":"2024-05-29T13:34:53.480582507Z","uplink_message":{"f_port":1,"f_cnt":110,"frm_payload":"MjYwRDBBNEM7MjkvNS8yMDI0OzEzOjU6NDQ7MjgyOC4wNjYyUzs2NTQ2LjAxNDJXOzEwODsA","rx_metadata":[{"gateway_ids":{"gateway_id":"eui-a84041ffff1f4cbc","eui":"A84041FFFF1F4CBC"},"time":"2024-05-29T13:34:53.081960Z","timestamp":1421259683,"rssi":-31,"channel_rssi":-31,"snr":7.2,"uplink_token":"CiIKIAoUZXVpLWE4NDA0MWZmZmYxZjRjYmMSCKhAQf//H0y8EKPn2qUFGgwI/d3csgYQ48bfgQEguOm2za6mAQ==","channel_index":2,"received_at":"2024-05-29T13:34:53.072001999Z"}],"settings":{"data_rate":{"lora":{"bandwidth":125000,"spreading_factor":7,"coding_rate":"4/5"}},"frequency":"917200000","timestamp":1421259683,"time":"2024-05-29T13:34:53.081960Z"},"received_at":"2024-05-29T13:34:53.275343967Z","consumed_airt..."';
//console.log(msjTTS);
//identifico a partir de que caracter empieza el dato en base64.
let cadenaAuxiliar = '"frm_payload":"';
let cadenaControl = msjTTS.indexOf(cadenaAuxiliar)+15; //320. Aca empieza el msj codificado en base64
//console.log(cadenaControl);

//identifico la cantidad de caracteres del mensaje en base64
let caracterDondeEmpiezaElMsj = cadenaControl;
let cantidadCaracteresDelMsjBase64 = 0;
do{
	caracter = msjTTS[cadenaControl];
	//console.log(caracter);
	cadenaControl = cadenaControl+1;
	cantidadCaracteresDelMsjBase64 = cantidadCaracteresDelMsjBase64+1;
}while(msjTTS[cadenaControl]!='"');
//console.log(cantidadCaracteresDelMsjBase64);

//extraemos el mensaje en base64 desde caracterDondeEmpiezaElMsj hasta cantidadCaracteresDelMsjBasse64.
let cadenaEnBase64 = msjTTS.slice(caracterDondeEmpiezaElMsj, caracterDondeEmpiezaElMsj+cantidadCaracteresDelMsjBase64);
//console.log(cadenaEnBase64);

//Transformamos el mensaje en Base64 a texto legible.
let cadenaDecodificada = atob(cadenaEnBase64);
//console.log(cadenaDecodificada);

//Colocamos en Variables los datos decodificados:
let id_animal;
let fecha;
let hora;
let latitud;
let posicion;
let nro_paquete;
//variables para controlar lo que extraemos del mensaje decodificado.
let caracterLeido = 0;
let cantidadCaracterDecodificado = 0;
do{//aca obtenemos la id_animal.
	cadenaDecodificada[cantidadCaracterDecodificado];
	cantidadCaracterDecodificado = cantidadCaracterDecodificado+1;
}while(cadenaDecodificada[cantidadCaracterDecodificado] != ';');
id_animal = cadenaDecodificada.slice(caracterLeido, cantidadCaracterDecodificado);
console.log(id_animal);
caracterLeido = cantidadCaracterDecodificado+1;
do{//aca obtenemos la fecha.
	cadenaDecodificada[cantidadCaracterDecodificado];
	cantidadCaracterDecodificado = cantidadCaracterDecodificado+1;
}while(cadenaDecodificada[cantidadCaracterDecodificado] != ';');
fecha = cadenaDecodificada.slice(caracterLeido, cantidadCaracterDecodificado);
console.log(fecha);
caracterLeido = cantidadCaracterDecodificado+1;
do{//aca obtenemos la hora.
	cadenaDecodificada[cantidadCaracterDecodificado];
	cantidadCaracterDecodificado = cantidadCaracterDecodificado+1;
}while(cadenaDecodificada[cantidadCaracterDecodificado] != ';');
hora = cadenaDecodificada.slice(caracterLeido, cantidadCaracterDecodificado);
console.log(hora);
caracterLeido = cantidadCaracterDecodificado+1;
do{//aca obtenemos la latitud.
	cadenaDecodificada[cantidadCaracterDecodificado];
	cantidadCaracterDecodificado = cantidadCaracterDecodificado+1;
}while(cadenaDecodificada[cantidadCaracterDecodificado] != ';');
latitud = cadenaDecodificada.slice(caracterLeido, cantidadCaracterDecodificado);
console.log(latitud);
caracterLeido = cantidadCaracterDecodificado+1;
do{//aca obtenemos la posicion.
	cadenaDecodificada[cantidadCaracterDecodificado];
	cantidadCaracterDecodificado = cantidadCaracterDecodificado+1;
}while(cadenaDecodificada[cantidadCaracterDecodificado] != ';');
posicion = cadenaDecodificada.slice(caracterLeido, cantidadCaracterDecodificado);
console.log(posicion);
caracterLeido = cantidadCaracterDecodificado+1;
do{//aca obtenemos la nro_paquete.
	cadenaDecodificada[cantidadCaracterDecodificado];
	cantidadCaracterDecodificado = cantidadCaracterDecodificado+1;
}while(cadenaDecodificada[cantidadCaracterDecodificado] != ';');
nro_paquete= cadenaDecodificada.slice(caracterLeido, cantidadCaracterDecodificado);
console.log(nro_paquete);
caracterLeido = cantidadCaracterDecodificado+1;
/*
//Transformamos el mensaje en Base64 a String o Hexadecimal. Para un entorno de Node.JS
let cadenaBuffer = Buffer.from(cadenaEnBase64, 'base64').toString('binary');
//Convertir la cadena binaria a un Uint8Array
const bytes = new Uint8Array(cadenaBuffer.length);
for (let i = 0; i < cadenaBuffer.length; i++) {
  bytes[i] = cadenaBuffer.charCodeAt(i);
}
// Decodificar el Uint8Array a una cadena UTF-8
const {TextDecoder} = require('util');
const cadenaDecodificada = new TextDecoder().decode(bytes);
console.log(cadenaDecodificada);
*/
//return msjTTS;

