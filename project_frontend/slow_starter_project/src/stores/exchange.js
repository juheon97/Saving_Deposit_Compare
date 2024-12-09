import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from 'axios'

export const useExchangeStore = defineStore("exchange", () => {
  const exchange_info = ref([]);

  const get_exchange_info = function() {
    axios({
      method:'get',
      url: 'http://127.0.0.1:8000/exchange/get_exchange_info/'
    })
    .then(res => {
      console.log(res.data)
      exchange_info.value =res.data
    })
  }

  return { exchange_info, get_exchange_info }
  
});
