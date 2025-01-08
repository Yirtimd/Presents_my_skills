<script>
import Gender_group from './components/gender_group.vue';
import Presents_data from './components/presents_data.vue';
import Rang_score from './components/rang_score.vue';
import Sort_by_skills from './components/sort_by_skills.vue';




export default {
  components: { Presents_data, Rang_score, Gender_group, Sort_by_skills }
}

</script>

<template>
  <h1>Presents my skills!</h1><br>
  <Presents_data/>
  <div class="button-row">
    <Rang_score/>
    <Gender_group/>
    <Sort_by_skills/>

  </div>

  

</template>

<style>

body {
  background-color: rgb(219, 222, 225);
}

h1 {
  text-align: center;
  color: rgb(19, 20, 20);
}

.button-row {
  display: flex; /* Выстраивает элементы в ряд */
  gap: 10px; /* Добавляет отступ между кнопками */
}


</style>
