<script setup>
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { reactive, ref, useTemplateRef } from 'vue';
import { useRouter } from 'vue-router';

const toastStore = useToastStore()
const userStore = useUserStore()
const router = useRouter()
const form = reactive({
    old_password: '',
    new_password1: '',
    new_password2: '',
    // avatar: null,
})

function submitForm() {
    errors.value = []
    if (form.new_password1 !== form.new_password2) {
        errors.value.push('The password does not match.')
    }

    if (errors.value.length === 0) {
        let formData = new FormData()
        formData.append('old_password', form.old_password)
        formData.append('new_password1', form.new_password1)
        formData.append('new_password2', form.new_password2)

        // console.log(formData)
        // console.log(this.$refs.file.files) not work🚩
        // console.log(file.value.files[0])
        axios
            .post('/api/editpassword/', formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            })
            .then(response => {
                // if (response.data.status === 'success') {
                if (response.data.message === 'password changed') {
                    toastStore.showToast(5000, 'The Information was saved.', 'bg-emerald-500')

                    router.push(`/profile/${userStore.user.id}`)
                } else {
                    // const data = JSON.parse(response.data)
                    const data = response.data.message
                    for (const key in data) {
                        errors.value.push(data[key][0].message)
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
                <h1 class="mb-6 text-2xl">Change Password</h1>
                <p class="mb-6 text-gray-500">
                    Here you can change your password.
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" @submit.prevent="submitForm">
                    <div>
                        <label>Old Password</label><br>
                        <input type="password" v-model="form.old_password" placeholder="Your old Password"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>New Password</label><br>
                        <input type="password" v-model="form.password1" placeholder="Your new Password"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Repeat Password</label><br>
                        <input type="password" v-model="form.password2" placeholder="Your new Password again"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
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