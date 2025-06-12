<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const notifications = ref([])
const router = useRouter()

function readNotify(notify) {
    axios
        .post(`/api/notifications/read/${notify.id}/`)
        .then(response => {
            console.log(response.data)
            if (notify.notification == 'postlike' || notify.notification == 'postcomment') {
                router.push({name: 'postview', params: {id: notify.post_id}})
            } else {
                router.push({name: 'friends', params: {id: notify.create_for_id}})
            }
        })
        .catch(err => {
            console.log(err)
        })
}

onMounted(() => {
    axios
        .get('/api/notifications/')
        .then(response => {
            notifications.value = response.data
            // console.log(response.data)
        })
        .catch(err => {
            console.log(err)
        })
})
</script>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div v-if="notifications.length" class="p-4 bg-white border border-gray-200 rounded-lg" v-for="notify in notifications" :key="notify.id">
                {{ notify.body }}
                <!-- <FeedItem :post="post" /> -->
                <button @click="readNotify(notify)" class="underline ml-4">READ MORE ...</button>
            </div>
            <div v-else class="p-4 bg-white border border-gray-200 rounded-lg">
                There is no UNREAD notifications for You.
            </div>
        </div>
    </div>
</template>