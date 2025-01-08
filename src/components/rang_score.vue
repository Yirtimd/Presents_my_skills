<script>
import axios from 'axios';
import { computed } from 'vue';

export default {
  data() {
    return {
      rang_score: [],
      buttonClickRangScore: false
    }
  },
  methods: {
    post_message() {
      const filter = this.buttonClickRangScore ? 'all' : 'rang_sort'
      const response = axios.get(`http://127.0.0.1:5000/rang_score?filter=${filter}`)
      this.rang_score = response.data;
      this.buttonClickRangScore = !this.buttonClickRangScore
    }
  }
}
</script>

<template>
    <div class="persons">
        <button @click="post_message()">
            <p>{{ buttonClickRangScore ? 'Скрыть' : 'Супергерои с очками силы выше: 85' }}</p>
        </button>
        <div v-show="buttonClickRangScore">
            <p> {{ rang_score }}</p>
        </div>
    </div>
  
</template>

<style>

</style>