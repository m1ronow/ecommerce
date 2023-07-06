import vue_number_input from './app.vue'

vue_number_input.install = function (Vue) {
    Vue.component(vue_number_input.name, vue_number_input);
};

export default vue_number_input;