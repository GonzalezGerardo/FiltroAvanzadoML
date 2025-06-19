<template>
  <div class="contenido">
    <h2>Tabla Detallada del Excel</h2>
    <div class="tabla-scroll">
      <table class="tableDetalles">
        <thead>
          <tr>
            <th v-for="(col, index) in columnasFiltradas" :key="index"
              :class="col === 'Titulo' ? 'columnaNombreProducto' : 'colCaracteristica'">
              {{ col }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(fila, index) in datos" :key="index">
            <td v-for="(col, colIndex) in columnasFiltradas" :key="colIndex"
              :class="col === 'Titulo' ? 'columnaNombreProducto' : 'colCaracteristica'">
              <template v-if="col === 'Titulo' && fila['Enlace']">
                <a :href="fila['Enlace']" target="_blank">{{ fila[col] }}</a>
              </template>
              <template v-else>
                {{ fila[col] }}
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      columnas: [],
      datos: []
    };
  },
  computed: {
    columnasFiltradas() {
      return this.columnas.filter(col => col !== 'Enlace');
    }
  },
  async created() {
    const res = await fetch('/caracteristicas.json');
    const json = await res.json();
    this.datos = json;
    this.columnas = Object.keys(json[0] || {});
  }
};
</script>