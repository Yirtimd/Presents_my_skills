<script>
import axios from 'axios';
import {io} from 'socket.io-client'
import { computed } from 'vue';
import Sort_by_skills from './sort_by_skills.vue';


export default {
  components: {Sort_by_skills}, 

  data() {
    return {
      info_message: [],
      select_skills: ['Flight', 'Super Strength', 'Heat Vision', 'Combat Skills', 'Lasso of Truth',
       'Intelligence', 'Martial Arts', 'Gadgets', 'Engineering', 'Powered Suit', 'Espionage', 'Hacking', 'Telekinesis'],
      buttonClick: false,
      showForm: false,
      formData: {
        person_name: "",
        gender: "",
        skills: [],
        power_score: ""
      },
      responseMessage: "",
      delete_name: {
        person_name: ""
      },
      select_hero: null
    }
  },
  methods: {
    post_message() {
      axios.post("http://127.0.0.1:5000/data")
      .then(res => {this.info_message = res.data})
    },
    submitForm () {
      this.showForm = !this.showForm
    },
    sendData() {
      const response = axios.post("http://127.0.0.1:5000/submit", this.formData);
      this.showForm = false;
      this.formData = {
        person_name: "",
        gender: "",
        skills: [],
        power_score: ""
      }
    },
    generate_hero() {
      const response = axios.get(`http://127.0.0.1:5000/generate_hero`)

    },
    deleteHero() {
      if (!this.select_hero) {
        alert("Выберите строку перед отправкой!");
        return;
      }
      axios.post("http://127.0.0.1:5000/delete", this.select_hero)
        .then(response => {
          console.log("Ответ сервера:", response.data);
        })
        .catch(error => {
          console.error("Ошибка при отправке данных:", error);
        });
        this.select_hero = null
    },
    selectRow(hero) {
      this.select_hero = hero; 
    }
    
  },
  mounted() {
    this.post_message();

    const socket = io("http://127.0.0.1:5000");
    
        // Обновление данных при событии "update_data"
    socket.on("update_data", (updatedHeroes) => {
      this.info_message = updatedHeroes;
    });
  }, 
  created () {
    axios.post("http://127.0.0.1:5000/data")
    .then(res => {this.info_message = res.data})
  }
}
</script>

<template>
  <div class="presents">
    <table class="table_data">
      <thead></thead>
      <tbody>
        <tr>
          <th>Супергерой:</th>
          <th>Пол:</th>
          <th>Суперсилы:</th>
          <th>Очки силы:</th>
        </tr>
        <tr v-for="(hero, index) in info_message" 
          :key="index" 
          @click="selectRow(hero)" 
          :class="{ selected: hero === select_hero }">
          <td>{{ hero['person_name'] }}</td>
          <td>{{ hero['gender'] }}</td>
          <td>{{ hero['skills'] }}</td>
          <td>{{ hero['power_score'] }}</td>
        </tr>
      </tbody>
    </table>
    <div>
      <button @click="submitForm" >Добавить героя</button>
      <form class="input_form" v-if="showForm" @submit.prevent="sendData">
  <!-- Поле имени и выбор гендера -->
        <div class="form-row">
          <div class="form-group">
            <label for="personal_name">Введите имя героя</label>
            <input type="text" id="personal_name" v-model="formData.person_name">
          </div>
          <div class="form-group">
            <label>Выберите пол героя</label>
            <div class="gender-options">
              <label>
                <input type="radio" value="Male" v-model="formData.gender">
                Male
              </label>
              <label>
                <input type="radio" value="Female" v-model="formData.gender">
                Female
              </label>
            </div>
          </div>
        </div>

        <!-- Навыки и очки мощи -->
        <div class="form-row">
          <div class="form-group">
            <label for="skills">Выберите навыки героя</label>
            <div v-for="(skill, index) in select_skills" :key="index">
              <label>
                <input 
                  type="checkbox" 
                  :value="skill" 
                  v-model="formData.skills"
                />
                {{ skill }}
              </label>
            </div>
          </div>
          <div class="form-group">
            <label for="power_score">Введите очки мощи героя</label>
            <input type="text" id="power_score" v-model="formData.power_score">
          </div>
        </div>

        <!-- Кнопка отправки -->
        <button type="submit">Отправить</button>
      </form>

    </div>
    <div>
      <button v-if="select_hero" @click="deleteHero">Удаление героя</button>
    </div>
    <div>
      <button @click="generate_hero">Сгенерировать героя</button>
    </div>
  </div>

</template>

<style scoped>
.selected {
  background-color: #c1bdbd;
}

table {
	width: 100%;
	border: none;
	margin-bottom: 20px;
}
table th {
	font-weight: bold;
	text-align: left;
	border: none;
	padding: 10px 15px;
	background: #686767;
	font-size: 14px;
  color: #fbf6f6;
}
table thead tr th:first-child {
	border-radius: 8px 0 0 8px;
}
table thead tr th:last-child {
	border-radius: 0 8px 8px 0;
}
table tbody td {
	text-align: left;
	border: none;
	padding: 10px 15px;
	font-size: 14px;
	vertical-align: top;
  
}

table tbody tr td:first-child {
	border-radius: 8px 0 0 8px;
}
table tbody tr td:last-child {
	border-radius: 0 8px 8px 0;
}

tr:hover {
  background-color: rgb(150, 147, 150);}


button {
  transition-duration: 0.2s;
  border-radius: 5px;
  font-size: 12px 16px;
  float: left;
}

button:hover {
  background-color: #3d62ae;
  color: white;
}

.input_form {
  display: flex;
  flex-direction: column;
  gap: 20px; /* Расстояние между строками */
}

.form-row {
  display: flex;
  justify-content: space-between;
  gap: 20px; /* Пространство между элементами строки */
}

.form-group {
  flex: 1; /* Элементы одной строки растягиваются равномерно */
}

.gender-options {
  display: flex;
  gap: 10px; /* Отступы между радио-кнопками */
}

input[type="text"], input[type="radio"], input[type="checkbox"] {
  margin-top: 5px; /* Небольшой отступ сверху для компактности */
  padding: 5px; /* Внутренний отступ для удобства ввода текста */
  font-size: 14px; /* Удобный размер текста */
}
</style>
