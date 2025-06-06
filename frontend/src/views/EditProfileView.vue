<script setup>
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { reactive, ref, useTemplateRef } from 'vue';
import { useRouter } from 'vue-router';

const toastStore = useToastStore()
const userStore = useUserStore()
const router = useRouter()
const file = useTemplateRef('file')
const form = reactive({
    email: userStore.user.email,
    name: userStore.user.name,
    // avatar: null,
})

function submitForm() {
    errors.value = []
    if (form.email === '') {
        errors.value.push('Your e-mail is missing')
    }

    if (form.name === '') {
        errors.value.push('Your name is missing')
    }

    if (errors.value.length === 0) {
        let formData = new FormData()
        formData.append('avatar', file.value.files[0])
        formData.append('name', form.name)
        formData.append('email', form.email)

        // console.log(formData)
        // console.log(this.$refs.file.files) not work🚩
        // console.log(file.value.files[0])
        axios
            .post('/api/editprofile/', formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            })
            .then(response => {
                // if (response.data.status === 'success') {
                if (response.data.message === 'Profile Updated.') {
                    toastStore.showToast(5000, 'The Information was saved.', 'bg-emerald-500')

                    userStore.setUserInfo({
                        id: userStore.user.id,
                        name: form.name,
                        email: form.email,
                    })
                    // form.email = ''
                    // form.name = ''
                    router.back()
                } else {
                    // const data = JSON.parse(response.data)
                    const data = response.data
                    for (const key in data) {
                        errors.value.push(data[key])
                    }

                    toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-red-300')
                }
            })
            .catch(error => {
                console.log('error', error)
            })
    }
}
const errors = ref([])
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
                        <label>AVATAR</label><br>
                        <!-- <input type="file" ref="file" class="file-input" @change="selectFile" multiple> -->
                        <input type="file" ref="file">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" :key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save Changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>