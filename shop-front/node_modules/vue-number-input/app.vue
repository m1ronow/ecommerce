<template>
    <div>
        <input type="number" v-if="keyboard=='number'" :placeholder="placeholder" @blur="$emit('blur')" @focus="$emit('focus')" v-model="inputValue">
        <input type="tel" v-else-if="keyboard=='tel'" :placeholder="placeholder" @blur="$emit('blur')" @focus="$emit('focus')" v-model="inputValue">
        <input type="text" v-else @blur="$emit('blur')" :placeholder="placeholder" @focus="$emit('focus')" v-model="inputValue">
    </div>
</template>

<script>
export default {
    name: 'vue-number-input',

    props: {
        type: {
            type: String,
            default: 'ufloat' // uint ufloat int float
        },
        value: {
            type: Number | String,
            required: false
        },
        maxLength: {
            type: Number,
            default: 999
        },
        split: {
            type: Number,
            default: 4
        },
        delimiter: {
            type: String,
            default: ''
        },
        decimalLength: {
            type: Number,
            default: 2
        },
        keyboard: {
            type: String,
            default: 'text'
        },
        placeholder: {
            type: String,
            default: '请输入'
        }
    },
    data() {
        return {
            inputValue: this.value
        }
    },
    watch: {
        inputValue: function(nv) {
            if (this.type == 'uint') {
                nv = nv.replace(/[^\d]/g, '')
                if (nv.length > this.maxLength) {
                    nv = nv.substring(0, this.maxLength)
                }

                if (this.delimiter) {
                    let reg = new RegExp("(\\d{" + this.split + "})", "g")
                    if (nv.length % this.split == 0) {
                        nv = nv.replace(reg, "$1" + this.delimiter)
                        nv = nv.substring(0, nv.length - 1)
                    } else {
                        nv = nv.replace(reg, "$1" + this.delimiter)
                    }
                }
            } else if (this.type == 'ufloat') {
                nv = nv.replace(/[^\d\.]/g, '')
                nv = nv.replace(/(\.\d+)\./g, '$1')
                nv = nv.replace(/\.\./g, '.')
                let reg = new RegExp("(\\d+\\.\\d{" + this.decimalLength + "})\\d+", "g")
                nv = nv.replace(reg, '$1')
            }
            this.inputValue = nv
            this.$emit('input', this.inputValue.replace(/[^\d\.-]/g, ''))
        }
    }
}
</script>

<style>

</style>
