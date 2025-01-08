<script>
import axios from 'axios';
import { computed } from 'vue';

export default {
  data() {
    return {
      gender_male: [],
      gender_female: [],
      buttonMale: false,
      buttonFemale: false,
    }
  },
  methods: {
    post_message_male() {
      const filter = this.buttonMale ? 'all' : 'male'
      axios.get(`http://127.0.0.1:5000/male?filter=${filter}`)
      .then(res => {this.gender_male = res.data});
      this.buttonMale = !this.buttonMale
    },
    post_message_female() {
      const filter = this.buttonFemale ? 'all' : 'female'
      axios.get(`http://127.0.0.1:5000/female?filter=${filter}`)
      .then(res => {this.gender_female = res.data})
      this.buttonFemale = !this.buttonFemale
    }
  }
}
</script>

<template>
    <div class="persons">
        <button @click="post_message_female()">
            <p>{{ buttonFemale ? 'Скрыть' : 'Супергерои женского пола' }}</p>
            <p v-show="buttonFemale" >{{ gender_female }}</p>
        </button>
        <button @click="post_message_male()">
            <p>{{ buttonMale ? 'Скрыть' : 'Супергерои мужского пола' }}</p>
            <p v-show="buttonMale" >{{ gender_male }}</p>
        </button>
    </div>

</template>

<style>

</style>