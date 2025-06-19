export async function resticciones(whiteList, blackList, setProductos/*, setLoading, setError*/) {
    //setLoading(true);
    //setError(false);
    setProductos([]);

    const payloadScrape = {
        permitido: convertirACadenaArray(whiteList),
        noPermitido: convertirACadenaArray(blackList)
    };
    function convertirACadenaArray(cadena) {
        // Si la cadena está vacía o solo tiene espacios, retorna arreglo vacío
        if (!cadena || cadena.trim() === '') {
            return [];
        }

        // Divide por comas, elimina espacios extra alrededor de cada palabra y filtra vacíos
        return cadena
            .split(',')
            .map(palabra => palabra.trim())
            .filter(palabra => palabra.length > 0);
    }

    try {
        console.log("Entra a Scrape")
        console.log("Datos:" + payloadScrape.permitido + payloadScrape.noPermitido)

        const resFiltro = await fetch('http://localhost:5000/filtrar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payloadScrape)
        });

        if (!resFiltro.ok) throw new Error('Error al filtrar productos');

        const productosFiltrados = await resFiltro.json();
        console.log("ResultadoL: " + productosFiltrados)
        setProductos(productosFiltrados);

    } catch (error) {
        console.error("Error general:", error);
        //setError(true);
    } finally {
        //setLoading(false);
    }
}