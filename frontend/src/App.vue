<template>
  <div>

    <div class="header">
      <h1>Filtro mejorado Mercado Libre</h1>
      <div class="formularioBusqueda">
        <div class="field fieldBusqueda">
          <p>Producto:</p>
          <input class="inputSearch" type="search" v-model="form.inputSearch" placeholder="Estoy buscando...">
        </div>
        <div class="field fieldPrecio">
          <p>Precio</p>
          <div class="fieldRangoPrecio">
            <input class="inputNumber" type="text" v-model="form.inputMin" placeholder="Min" />
            <input class="inputNumber" type="text" v-model="form.inputMax" placeholder="Max" />
          </div>
        </div>
        <div class="field">
          <button class="btnBuscar" @click="filtrarProductos">Buscar</button>
        </div>
      </div>
      <!-- MENSAJE DE CARGA -->
      <div v-if="loading" class="mensajeCarga">
        <p>Cargando productos...</p>
      </div>
      <div v-if="error" class="mensajeCarga">
        <p>Error al obtener los productos. Intenta de nuevo.</p>
      </div>
    </div>

    <button @click="tab = 'resumen'">Resumen</button>
    <button @click="tab = 'detalles'">Detalles</button>

    <TablaSimple v-if="tab === 'resumen'" :productos="productos" :key="productos.length + '_' + Date.now()" />
    <Detalles v-if="tab === 'detalles'" />
  </div>
</template>


<script>
import TablaSimple from './components/TablaSimple.vue';
import Detalles from './components/Detalles.vue';

import { filtrarProductos } from './utils/app.js';

export default {
  components: { TablaSimple, Detalles },
  data() {
    return {
      tab: 'resumen',
      form: {
        inputSearch: 'Tarjeta grafica NVIDIA 4060',
        inputMin: '',
        inputMax: ''
      },
      productos: [],
      loading: false,
      error: false
    };
  },
  methods: {
    filtrarProductos() {
      filtrarProductos(
        this.form,
        productos => this.productos = productos,
        estado => this.loading = estado,
        estado => this.error = estado
      );
    }
  }
};
</script>