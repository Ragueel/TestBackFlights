<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
    <v-data-table
      :headers="headers"
      :items="data"
      class="elevation-1" 
      v-if="!isLoading"
    ></v-data-table>
    <div v-else>
      <v-skeleton-loader class="mx-auto" type="table"></v-skeleton-loader>
    </div>
    </v-col>
  </v-row>
</template>
<script>
export default {
  data:()=>{
    return {
      headers:[
        {text: 'From',align:'start',sortable:false, value:'flight_from'},
        {text: 'To',align:'start',sortable:false, value:'flight_to'},
        {text: 'Price',align:'start',sortable:false, value:'price'},
      ],
      isLoading: true,
      data: []
    }
  },
  mounted() {
    this.isLoading = true;
    this.$axios.get('/api/v1/flights').then(response=>{
      this.isLoading = false;
      this.data = response.data.data;
      console.log(response);
    }).catch(err=>{
      console.log(err);
    });
  },
}
</script>
