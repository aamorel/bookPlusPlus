<template class="templ" lang="html">

  <div class="container">
    <Head/>
    <div class="divInput">
      <form  class="form" v-if="starting" @submit="addText">
        <textarea class="textInput" spellcheck="false" rows="15"  v-model="textForm" name="textForm" placeholder="Submit your text and be ready"/>
        <b-button class="but" type="submit"> GO ! </b-button>
      </form>

    </div>
    <div class="que">
      <form  class="formb" v-if="queryAsk" @submit="addQuery" spellcheck="false">
        <input class="textIn" type="text" v-model="queryForm" name="textForm" placeholder="Keywords to find what you are looking for">
        <b-button class="buto" type="submit"> Show me! </b-button>
        <!-- <input type="range" min="1" max="5" v-model="nb"> -->
        <circle-slider  class="slider" v-model="nb"  :side="70"  :min="1"  :max="4"  :step-size="1"  :circle-width-rel="5"  :progress-width-rel="10"  :knob-radius="5"></circle-slider>
        <p class="phrase"> Paragraphs </p>
        <p class="num"> {{nb}} </p>
        <b-form-group class="radio">
          <b-form-radio-group required="true" v-model="selected" :options="options" name="buttons-1" buttons></b-form-radio-group>
        </b-form-group>
      </form>

    </div>
    <<h1 v-if="para" class="sub">Requested Paragraphs</h1>
    <div class="paras" v-for="p in paragraphs" :key="p.id">

      <textarea class="paragraphs" spellcheck="false" readonly="true" rows="10">  {{p.text}}  </textarea>
      <textarea class="paradeux" spellcheck="false" readonly="true" rows="3">  {{p.sentence}}. </textarea>
      <p v-if="selected == 'vague'" class="der"> Main Info: </p>
    </div>





    <form  class="reload" v-if="para" @submit="reload">
      <b-button class="buto" type="submit"> New text! </b-button>
    </form>


    <div  class="divInput" v-for="t in texts" :key="40">
      <h1 v-if= "para" class="subi">Original Text</h1>
      <textarea class="text" readonly="true" spellcheck="false" rows="30">  {{t.text}}  </textarea>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import Head from "./Head.vue";

export default {
  data() {
    return {
      selected: '',
      options: [
        {text: 'Precise Request', value: 'precise'},
        {text: 'Vague Search', value: 'vague'}
      ],
      starting: true,
      query: false,
      queryAsk: false,
      para: false,
      texts: [],
      textForm: '',
      queryForm:'',
      nb: 1,
      paragraphs: [],
      radio: true
    };
  },
  components: {
    Head
  },
  methods: {
    getTexts() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
        .then((res) => {
          if (!this.query) {
            this.texts = res.data.books;
            console.log("returned text")
          }
          else {
            console.log("returned paragraphs");
            this.queryAsk = false;
            this.paragraphs = res.data.books;

            this.para = true;
          }




        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    highlight(p) {

       return append(p.text.replace(new RegExp(p.sentence, "gi"), match => {
          return '<span class="highlightText">' +  match + '</span>'
      }));

    },
    reload(e){
      e.preventDefault();
      this.selected = '';
      this.options = [
        {text: 'Precise Request', value: 'precise'},
        {text: 'Vague Search', value: 'vague'}
      ];
      this.starting = true;
      this.query = false;
      this.queryAsk = false;
      this.para = false;
      this.texts = [];
      this.textForm = '';
      this.queryForm = '';
      this.nb = 1;
      this.paragraphs =  [];
      this.radio = true;
    },
    addText(e) {
      e.preventDefault();
      this.starting = false;
      console.log("this.textForm");

      const textToSend = {
        'id': 1,
        'text': this.textForm
      }

      const path = 'http://localhost:5000/books';
      axios.post(path, textToSend)
        .then(() => {
          this.query = false;
          this.queryAsk = true;
          this.getTexts();

        })
        .catch((error) => {

        });
      this.query = true;
    },
    addQuery(e) {
      e.preventDefault();
      console.log(this.selected);
      this.query = false;
      document.documentElement.style.setProperty('--my-variable-name', 80/this.nb + '%');
      const queryToSend = {
        'id': 2,
        'myQuery': this.queryForm,
        'nbPar': this.nb,
        'mode': this.selected
      }
      const path = 'http://localhost:5000/books';
      axios.post(path, queryToSend)
        .then(() => {
          console.log('Query is sent');
          this.query = true;
          this.getTexts();


        })

        .catch((error) => {

        });
        this.query = false;
    }


  }
};
</script>

<style lang="css" scoped>
:root {
    --my-variable-name: 0;
}

.paragraphs{

  width: 50%;
  margin: auto;
  border: none;
  border-radius: 10px;
	padding: 5px;
	font-family: Tahoma, sans-serif;
  background-color: #F0F8FF;

}
.paradeux{

  width: 50%;
  margin: auto;
  margin-bottom: 50px;
  border: none;
  border-radius: 10px;
	padding: 5px;
	font-family: Tahoma, sans-serif;
  font-style: italic;


}

.paras{
  text-align: center;
}
.text{
  width: 90%;
  margin:auto;
  border: 3px solid #cccccc;
	padding: 10px;
	font-family: Tahoma, sans-serif;
}
.textInput{
  width: 90%;
  border-radius: 10px;

}
.sub{
  font-family: Tahoma, sans-serif;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}
.subi{
  font-family: Tahoma, sans-serif;
  font-size: 20px;

}
.but{
  text-align: left
}
.divInput{
  margin: auto;
  display: block;
  text-align: center;
  position: relative;
}
.form{
  position: relative;

}
.formb{
  position: relative;
  border-style: solid;
  border-color: #6D747E;
  border-width: 3px;
  border-radius: 10px;
  height: 150px;
  background-color: white;
}
.but{
  position: absolute;
  top: 10px;
  right: 65px;
  width: 100px;
}
.buto{
  text-align: center;
  position: absolute;
  padding-bottom: 30px;
  background-color: #FF8E88;
  border: none;
  top: 100px;
  right: 600px;
  width: 100px;
  height: 30px;
}
.que{
  margin-bottom: 30px;
}
.textIn{
  width: 50%;
  position: absolute;
  right: 350px;
  top: 60px;
}
.slider{
  position:absolute;
  top: 30px;
  left: 30px;
}
.num{
  position:absolute;
  left: 53px;
  top: 35px;
  font-size: 40px;
}
.phrase{
  position: absolute;
  top: 100px;
  left: 27px;
}

.radio{
  position: absolute;
  top: 55px;
  right: 30px;
}
.highlightText {
        background: yellow;
    }
.der{
  color:#1BBC9B;
  position: relative;
  top: -160px;
  left: 250px;
  font-weight: bold;
}
</style>
