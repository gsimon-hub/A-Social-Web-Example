<script setup>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
// import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { onMounted, reactive, ref } from 'vue';
import {  useRoute } from 'vue-router';

const friends = ref([])
const user = reactive({})
const friendship_requests = ref([])
// const userStore = useUserStore()
const route = useRoute()

function getFriends() {
    axios
        .get(`/api/friends/${route.params.id}/`)
        .then(response => {
            friends.value = response.data.friends
            friendship_requests.value = response.data.requests
            Object.assign(user, response.data.user)
        })
        .catch(error => {
            console.log('error', error)
        })
}

function handleRequests(status, pk) {
    console.log('handleRequests: ', status)
    axios
        .post(`/api/friends/${pk}/${status}/`)
        .then(response => {
            console.log(status, ':---', response.data)
        })
        .catch(error => {
            console.log(error)
        })
}

onMounted(() => getFriends())
</script>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name: 'friends', params:{id: user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <!-- <div v-if="friends.length" class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4"> -->
            <div v-if="friendship_requests.length" class="p-4 bg-white border border-gray-200 rounded-lg">
                <h2 class="mb-6 text-xl">FriendShip Requests</h2>
                <div v-for="request in friendship_requests" :key="request.id" class="p-4 text-center bg-gray-100 rounded-lg">
                    <!-- <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full"> -->
                    <img src="https://i.pravatar.cc/100?img=70" class="mb-6 mx-auto rounded-full">

                    <p>
                        <strong>
                            <RouterLink :to="{ name: 'profile', params: { 'id': request.created_by.id } }">
                                {{ request.created_by.name }}
                            </RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                        <p class="text-xs text-gray-500">120 posts</p>
                    </div>

                    <div class="mt-6 space-x-4">
                        <button @click="handleRequests('accepted', request.created_by.id)" class="inline-block py-4 px-6 bg-purple-600 text-xs text-white rounded-lg">Accept</button>
                        <button @click="handleRequests('rejected', request.created_by.id)" class="inline-block py-4 px-6 bg-red-600 text-xs text-white rounded-lg">Reject</button>
                    </div>
                </div>
                
            </div>
            
            <hr v-if="friendship_requests.length"> 

            <div v-if="friends.length" class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4">
                <div v-for="friend in friends" :key="friend.id" class="p-4 text-center bg-gray-100 rounded-lg">
                    <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

                    <p>
                        <strong>
                            <RouterLink :to="{ name: 'profile', params: { 'id': friend.id } }">
                                {{ friend.name }}
                            </RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                        <p class="text-xs text-gray-500">120 posts</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>
