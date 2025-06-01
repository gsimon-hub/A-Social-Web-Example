<script setup lang="ts">
import { RouterLink } from 'vue-router';
import axios from 'axios';
import { reactive, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import router from '@/router';

const userStore = useUserStore()

const form = reactive({
    email: '',
    password: '',
})
const errors = ref([])

function submitForm() {
    errors.value = []

    if (form.email === '') {
        errors.value.push('Your email is missing')
    }

    if (form.password === '') {
        errors.value.push('Your password is missing')
    }

    if (errors.value.length === 0) {
        axios
            .post('/api/login/', form)
            .then(response => {
                userStore.setToken(response.data)
                axios.defaults.headers.common['Authorization'] = "Bearer " + response.data.access
                // console.log("setToken finished: ", axios.defaults.headers.common['Authorization'])
            })
            .catch(error => {
                errors.value.push(error)
            })
            
        axios
            .get('/api/me/')
            .then(response => {
                userStore.setUserInfo(response.data)
                router.push('/feed')
                // console.log("setToken finished: ", axios.defaults.headers.common['Authorization'])
            })
            .catch(error => {
                errors.value.push(error)
            })
    }
}

</script>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Log In</h1>
                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                </p>
                <p class="font-bold">
                    Don't have an account? <RouterLink to="/signup" class="underline">Click here</RouterLink> to Create
                    one!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" @submit.prevent="submitForm">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" v-model="form.password" placeholder="Your password"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>
                    
                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" :key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log In</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>