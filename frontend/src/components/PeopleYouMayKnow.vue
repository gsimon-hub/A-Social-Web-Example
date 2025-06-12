<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const friends_suggestions = ref([])

onMounted(() => {
    axios
        .get('/api/friends/suggested/')
        .then(response => {
            console.log(response.data)
            friends_suggestions.value = response.data
        })
        .catch(err => {
            console.log(err)
        })
})
</script>

<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">People you may know</h3>

        <div class="space-y-4">
            <div v-for="friend in friends_suggestions" :key="friend.id" class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <img :src="friend.get_avatar" class="w-[40px] rounded-full">

                    <p class="text-xs"><strong>{{ friend.name }}</strong></p>
                </div>

                <RouterLink :to="{name: 'profile', params: {id: friend.id}}" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Show</RouterLink>
            </div>
        </div>
    </div>
</template>