msg.latitud = convertirCoordenadas (msg.latitud);

msg.longitud = convertirCoordenadas(msg.longitud);

msg.datoCargable = datoFinalParaCargar;
return msg;

function convertirCoordenadas(numeroConLetra) {

    let letra = numeroConLetra.slice(-1);  // Toma la última letra (N, S, E, O, etc.)
    let numero = parseFloat(numeroConLetra.slice(0, -1));//pasamos el string a numero para poder operar

    let grados = Math.floor(parseFloat(numero) / 100);//calculamos y guardamos los datos

    let minutosDecimales = (parseFloat(numero) % 100) /100;//tomamos el resto de los los grados


    let minutos = Math.floor(minutosDecimales * 60);//calculamos y separamos los grados

    let segundosDecimales = (minutosDecimales * 60)-minutos;//tomamos el resto de los minutos 

    let segundos = segundosDecimales * 60;//calculamos los segundos
    let convertida = `${grados}°${minutos}'${segundos.toFixed(4)}"${letra}`;//volmemos a poner todo en un string
    return convertida;
}