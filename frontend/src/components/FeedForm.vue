<script setup>
import axios from 'axios'
import {  ref, useTemplateRef } from 'vue'

defineProps(['user', 'posts'])

// const user = reactive({})
const body = ref('')
// const posts = ref([])
const is_private = ref('')
const url = ref(false)
const file = useTemplateRef('file')

function submitForm() {
    // console.log('submitForm', body.value)
    let formData = new FormData()
    formData.append('image', file.value.files[0])
    // console.log('files: ', file.value.files)
    formData.append('body', body.value)
    formData.append('is_private', is_private.value)
    axios
        // .post('/api/posts/create/', {
        //     'body': body.value
        // })
        .post('/api/posts/create/', formData, {
            Headers: {
                "Content-Type": "multipart/form-data",
            }
        })
        .then(response => {
            console.log('data', response.data)
            posts.value.unshift(response.data)
            user.posts_count += 1
            body.value = ''
            is_private.value = false
            url.value = null
        })
        .catch(error => {
            console.log('error', error)
        })
}

function onFileChange(e) {
    const file = e.target.files[0]
    url.value = URL.createObjectURL(file)
}
</script>

<template>
    <form method="post" @submit.prevent="submitForm">
        <div class="p-4">
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
            
            <div id="preview" v-if="url">
                <img :src="url" class="w-[100px] mt-3 rounded-xl ">
            </div>
            
            <label>
                <input type="checkbox" v-model="is_private"> Private
            </label>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                <input type="file" ref="file" @change="onFileChange">
                Attach Image
            </label>
            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>

<style>
input[type="file"] {
    display: none;
}

.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>