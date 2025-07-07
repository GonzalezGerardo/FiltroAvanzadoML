export async function filtrarProductos(form, setProductos, setLoading, setError) {
    setLoading(true);
    setError(false);
    setProductos([]);



    const inputMin = form.inputMin == '' ? '0' : form.inputMin;
    const inputMax = form.inputMax == '' ? '0' : form.inputMax;

    const payloadScrape = {
        product_name: form.inputSearch,
        minimal_price_limit: inputMin,
        maximal_price_limit: inputMax
    };

    console.log("Entra función filtrar")

    if (form.inputSearch !== null) {
        try {
            // PRIMERA PETICIÓN: Obtener productos sin filtrar
            const resScrape = await fetch('http://localhost:5000/scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payloadScrape)
            });

            const productosCrudos = await resScrape.json();

            if (!resScrape.ok) throw new Error('Error al filtrar productos');
            setProductos(productosCrudos);

        } catch (error) {
            console.error("Error general:", error);
            setError(true);
        } finally {
            setLoading(false);
        }
    }
}