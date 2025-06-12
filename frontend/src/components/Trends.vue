<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'

const trends = ref('')

onMounted(() => {
    axios
        .get('/api/posts/trends/')
        .then(response => {
            // console.log(response.data)
            trends.value = response.data
        })
        .catch(err => {
            console.log(err)
        })
})

</script>

<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">Trends</h3>

        <div class="space-y-4">
            <div v-for="trend in trends" :key="trend.id" class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <p class="text-xs">
                        <strong>{{ trend.hashTag }}</strong><br>
                        <span class="text-gray-500">{{ trend.occurences }} posts</span>
                    </p>
                </div>

                <RouterLink :to="{name: 'trendview', params: {id: trend.hashTag}}" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</RouterLink>
            </div>
        </div>
    </div>
</template>