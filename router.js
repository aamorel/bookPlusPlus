import Vue from 'vue';
import Router from 'vue-router';
import Text from './components/Text.vue';
import VueCircleSlider from 'vue-circle-slider'
import PrettyCheckbox from 'pretty-checkbox-vue';

Vue.use(PrettyCheckbox);

Vue.use(VueCircleSlider)



Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Text',
      component: Text,
    },
  ],
});
