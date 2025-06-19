<template>
  <div class="contenido">
    <h2>Productos Resumidos</h2>

    <div class="formularioFiltro">
      <div class="field fieldBlackList">
        <p>Palabras permitidas:</p>
        <input class="inputBlackList" type="text" v-model="whiteList"
          placeholder="Ej.: Tarjeta grafica, tarjeta de video, tarjeta...">
      </div>

      <div class="field fieldBlackList">
        <p>Palabras prohibidas:</p>
        <input class="inputBlackList" type="text" v-model="blackList" placeholder="Ej.: Adaptador, " />
      </div>
      <div class="field">
        <button class="btnBuscar" @click="resticciones">Aplicar</button>
      </div>
    </div>


    <table class="tableSimple">
      <thead>
        <tr>
          <th class="columnaNombreProducto">Título</th>
          <th>Precio</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in productos" :key="item.Titulo">
          <td class="columnaNombreProducto"><a :href="item.Enlace" target="_blank">{{ item.Titulo }}</a></td>
          <td>${{ item.Precio }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import { resticciones } from '../utils/tablaSimple.js';

export default {
  data() {
    return {
      whiteList: '',
      blackList: '',
      productos: []
    };
  },
  async created() {
    const res = await fetch('/productosV1.json');
    this.productos = await res.json();
  },
  methods: {
    resticciones() {
      resticciones(
        this.whiteList,
        this.blackList,
        productos => this.productos = productos
      );
    }
  }
};
</script>