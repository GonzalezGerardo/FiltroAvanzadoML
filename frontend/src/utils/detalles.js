export async function fetchProducts(form, setProductos, setLoading, setError) {
    setLoading(true);
    setError(false);
    setProductos([]);

    const payloadScrape = {
        product_name: form.product_name,
        minimal_price_limit: form.minimal_price_limit,
        maximal_price_limit: form.maximal_price_limit
    };

    try {
        console.log("Entra a Scrape")
        console.log("Datos:" +
            form.product_name + form.minimal_price_limit + form.maximal_price_limit
        )
        const resScrape = await fetch('http://localhost:5000/scrape', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payloadScrape)
        });

        const productosCrudos = await resScrape.json();

        const payloadFiltro = {
            productos: productosCrudos,
            palabras_clave_inicio: form.palabras_clave_inicio.split(',').map(p => p.trim().toLowerCase()),
            palabras_prohibidas: form.palabras_prohibidas.split(',').map(p => p.trim().toLowerCase())
        };

        const resFiltro = await fetch('http://localhost:5000/filtrar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payloadFiltro)
        });

        if (!resFiltro.ok) throw new Error('Error al filtrar productos');

        const productosFiltrados = await resFiltro.json();
        setProductos(productosFiltrados);

    } catch (error) {
        console.error("Error general:", error);
        setError(true);
    } finally {
        setLoading(false);
    }
}

export async function filtrarProductos(form, setProductos, setLoading, setError) {
    setLoading(true);
    setError(false);
    setProductos([]);

    const payloadScrape = {
        product_name: form.product_name,
        minimal_price_limit: form.minimal_price_limit,
        maximal_price_limit: form.maximal_price_limit
    };

    console.log("Entra función filtrar")
    console.log("Datos:" +
        form.product_name + "\t" + form.minimal_price_limit + "\t" + form.maximal_price_limit
    )
    if (form.product_name !== null && form.minimal_price_limit !== null && form.maximal_price_limit !== null) {
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