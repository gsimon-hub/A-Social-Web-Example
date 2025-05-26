<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { useToastStore } from '@/stores/toast';
// import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()
const form = reactive({
    email: '',
    name: '',
    password1: '',
    password2: ''
})
const errors = ref([])

function submitForm() {
    errors.value = []
    
    if (form.email === '') {
        errors.value.push('Your e-mail is missing')
    }

    if (form.name === '') {
        errors.value.push('Your name is missing')
    }

    if (form.password1 === '') {
        errors.value.push('Your password is missing')
    }

    if (form.password1 !== form.password2) {
        errors.value.push('The password does not match')
    }

    if (errors.value.length === 0) {
        axios
            .post('/api/signup/', form)
            .then(response => {
                // if (response.data.status === 'success') {
                if (response.status === 200) {
                    toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking your email link.', 'bg-emerald-500')

                    form.email = ''
                    form.name = ''
                    form.password1 = ''
                    form.password2 = ''
                } else {
                    // const data = JSON.parse(response.data)
                    const data = response.data
                    for (const key in data) {
                        errors.value.push(data[key])
                    }

                    toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
                }
            })
            .catch(error => {
                console.log('error', error)
            })
    }
}
// export default {
//     setup() {
//         const toastStore = useToastStore()

//         return {
//             toastStore
//         }
//     },

//     data() {
//         return {
//             form: {
//                 email: '',
//                 name: '',
//                 password1: '',
//                 password2: ''
//             },
//             errors: [],
//         }
//     },

//     methods: {
//         submitForm() {
//             this.errors = []

//             if (this.form.email === '') {
//                 this.errors.push('Your e-mail is missing')
//             }

//             if (this.form.name === '') {
//                 this.errors.push('Your name is missing')
//             }

//             if (this.form.password1 === '') {
//                 this.errors.push('Your password is missing')
//             }

//             if (this.form.password1 !== this.form.password2) {
//                 this.errors.push('The password does not match')
//             }

//             if (this.errors.length === 0) {
//                 axios
//                     .post('/api/signup/', this.form)
//                     .then(response => {
//                         if (response.data.message === 'success') {
//                             this.toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking your email link.', 'bg-emerald-500')

//                             this.form.email = ''
//                             this.form.name = ''
//                             this.form.password1 = ''
//                             this.form.password2 = ''
//                         } else {
//                             const data = JSON.parse(response.data.message)
//                             for (const key in data) {
//                                 this.errors.push(data[key][0].message)
//                             }//                             this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
//                         }
//                     })
//                     .catch(error => {
//                         console.log('error', error)
//                     })
//             }
//         }
//     }
// }
</script>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Sign Up</h1>
                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                </p>
                <p class="font-bold">
                    <!-- Already have an account? <a href="#" class="underline">Click here</a> to log in! -->
                    Already have an account? <RouterLink to="/login" class="underline">Click here</RouterLink> to log
                    in!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" @submit.prevent="submitForm">
                    <div>
                        <label>Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Your Full Name"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" v-model="form.password1" placeholder="Your password"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Repeat Password</label><br>
                        <input type="password" v-model="form.password2" placeholder="Password again"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" :key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign Up</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>