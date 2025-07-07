from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['POST'])
def scrape():
    print("++++++++++++++++++++++++++ Entra \"scrape\" ++++++++++++++++++++++++++")
    data = request.get_json()

    product_name = data.get('product_name', '').strip()
    minimal_price_limit = data.get('minimal_price_limit')
    maximal_price_limit = data.get('maximal_price_limit')

    # Validar campos obligatorios
    if not product_name:
        return jsonify({"error": "El nombre del producto es obligatorio"}), 400

    try:
        minimal_price_limit = int(minimal_price_limit)
        maximal_price_limit = int(maximal_price_limit)
    except (ValueError, TypeError):
        return jsonify({"error": "Los límites de precio deben ser números válidos"}), 400
    #Llamar al metodo de Scraping
    productos = hacer_scraping(product_name, minimal_price_limit, maximal_price_limit)
    with open('./frontend/public/productosV1.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(productos, jsonfile, ensure_ascii=False, indent=4)
    return jsonify(productos)


@app.route('/filtrar', methods=['POST'])
def filtrar():
    print("++++++++++++++++++++++++++ Entra \"filtrar\" ++++++++++++++++++++++++++")
    data = request.get_json()
    print("data recibida:", data)
    #abrir archivo
    with open("./frontend/public/productosV1.json", "r", encoding="utf-8") as f:
        dataDoc = json.load(f)

        # Recolectar todos los nombres de características posibles

    rows = []
    for producto in dataDoc:
        row = {}
        row["Titulo"] = producto["Titulo"]
        row["Precio"] = producto["Precio"]
        row["Enlace"] = producto["Enlace"]
        rows.append(row)
    print("row" + str(data))
    productos_filtrados = []

    for producto in rows:
        titulo = producto.get('Titulo', '').lower()
        # Validar palabras prohibidas
        if any(palabra in titulo for palabra in data.get('noPermitido', '')):
            continue
        # Validar que el título empiece con alguna palabra clave
        if data.get('permitido', '') and not any(titulo.startswith(palabra) for palabra in data.get('permitido', '')):
            continue

        productos_filtrados.append(producto)

    with open('./frontend/public/productosV2.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(productos_filtrados, jsonfile, ensure_ascii=False, indent=4)
    return jsonify(productos_filtrados)


def hacer_scraping(product_name, minimal_price_limit, maximal_price_limit):
    print("---------------------------------------------------- hacer_scraping ----------------------------------------------------")
    print(f"Variables:\nproduct_name: {product_name}\tminimal_price_limit: {minimal_price_limit}\tmaximal_price_limit: {maximal_price_limit}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    products = []
    #Separar por comas
    buscando = [item.strip() for item in product_name.split(",") if item.strip()]
    for producto in buscando:
        products += extraerInfo(producto, minimal_price_limit, maximal_price_limit, headers)
        

    print("Productos encontrados:", len(products))
    return products

def extraerInfo(product_name, minimal_price_limit, maximal_price_limit, headers):
    products=[]
    print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("Extrayendo información de: "+product_name)
    print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    
    for repeticion in range(30):
        rango = f'_Desde_{repeticion * 50 + 1}' if repeticion > 0 else ''
        if minimal_price_limit == "0" and maximal_price_limit == "0":
            url = (
                f'https://listado.mercadolibre.com.mx/{product_name.replace(" ", "-")}{rango}_OrderId_PRICE'
                f'ITEM*CONDITION_2230284_NoIndex_True_SHIPPING*ORIGIN_10215068'
            )
        else:
            url = (
                f'https://listado.mercadolibre.com.mx/{product_name.replace(" ", "-")}{rango}_OrderId_PRICE'
                f'_PriceRange_{minimal_price_limit}-{maximal_price_limit}_'
                f'ITEM*CONDITION_2230284_NoIndex_True_SHIPPING*ORIGIN_10215068'
            )
        print("URL usada: "+url)
        response = requests.get(url, headers=headers)
        if(response.status_code != 200):
            print("Error 404, terminando proceso")
            break

        print("Response status:", response.status_code)
        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.select('.poly-card'):
            title_tag = item.select_one('.poly-component__title-wrapper')
            price_tag = item.select_one('.andes-money-amount__fraction')
            link_tag = item.select_one('.poly-component__title')

            if title_tag and price_tag and link_tag:
                products.append({
                    'Titulo': title_tag.text.strip(),
                    'Precio': price_tag.text.strip(),
                    'Enlace': link_tag['href'],
                    'Caracteristicas': {}
                })
    return products

    #termina Scraping



@app.route('/scrape2', methods=['POST'])
def scrape2():
    data = request.json

    product_name = data.get('product_name', 'Tarjeta grafica')
    minimal_price_limit = data.get('minimal_price_limit', '2500')
    maximal_price_limit = data.get('maximal_price_limit', '4500')
    palabras_clave_inicio = data.get('palabras_clave_inicio', ['grafica', 'tarjeta', 'nvidia', 'rtx'])
    palabras_prohibidas = data.get('palabras_prohibidas', ['amd', 'radeon', 'monitor', 'bebe', 'mascota', 'auto', 'carro', 'niño', 'niña', 'comedor', 'bar', 'jardín', 'jardin'])

    def get_products():
        headers = {'User-Agent': 'Mozilla/5.0'}
        products = []
        for repeticion in range(10):
            rango = f'_Desde_{repeticion * 50 + 1}' if repeticion > 0 else ''
            url = f'https://listado.mercadolibre.com.mx/{product_name.replace(" ", "-")}{rango}_OrderId_PRICE_PriceRange_{minimal_price_limit}-{maximal_price_limit}_ITEM*CONDITION_2230284_NoIndex_True_SHIPPING*ORIGIN_10215068'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            for item in soup.select('.poly-card'):
                title_tag = item.select_one('.poly-component__title-wrapper')
                price_tag = item.select_one('.andes-money-amount__fraction')
                link_tag = item.select_one('.poly-component__title')
                if title_tag and price_tag and link_tag:
                    products.append({
                        'Titulo': title_tag.text.strip(),
                        'Precio': price_tag.text.strip(),
                        'Enlace': link_tag['href']
                    })
        print("-------------------------------products-------------------------------")            
        print(products)
        return products

    def titulo_valido(titulo):
        titulo = str(titulo).lower().strip()
        return any(titulo.startswith(p) for p in palabras_clave_inicio) and not any(p in titulo for p in palabras_prohibidas)

    def extraer_detalles(link):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            descripcion_tag = soup.find('p', {'class': 'ui-pdp-description__content'})
            descripcion = descripcion_tag.text.strip() if descripcion_tag else 'No disponible'
            claves_tags = soup.select('.andes-table__header')
            valores_tags = soup.select('.andes-table__column')
            caracteristicas = {
                claves_tags[i].get_text(strip=True): valores_tags[i].get_text(strip=True)
                for i in range(min(len(claves_tags), len(valores_tags)))
            }
            return descripcion, caracteristicas
        except Exception as e:
            print(f"Error al procesar {link}: {e}")
            return 'Error', {}

    # Proceso principal
    products = get_products()
    df = pd.DataFrame(products)
    df_filtrado = df[df['Titulo'].apply(titulo_valido)]
    df_filtrado.to_csv('./frontend/public/productos.csv', index=False)

    detalles = []
    for _, row in df_filtrado.iterrows():
        descripcion, caracteristicas = extraer_detalles(row['Enlace'])
        detalles.append({
            'Titulo': row['Titulo'],
            'Precio': row['Precio'],
            'Enlace': row['Enlace'],
            'Descripcion': descripcion,
            'Caracteristicas': caracteristicas
        })
        time.sleep(1)

    with open('./frontend/public/productos_detallados.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(detalles, jsonfile, ensure_ascii=False, indent=4)
    return jsonify(detalles)

if __name__ == '__main__':
    app.run(debug=True)
