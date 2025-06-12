<script setup>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { onMounted, ref, watch, reactive } from 'vue';
import { onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router';
import FeedItem from '@/components/FeedItem.vue';
import { useToastStore } from '@/stores/toast';
import FeedForm from '@/components/FeedForm.vue';
// import router from '@/router';

const posts = ref([])
const user = reactive({})

const userStore = useUserStore()
const toastStore = useToastStore()
// useRoute, not useRouter 🚩
const route = useRoute()
const router = useRouter()

// computed() line not needed for this script 🚩
// const user_id = computed(() => route.params.id);
// console.log('user', route.params.id)

function sendFriendshipRequest() {
    axios
        .post(`/api/friends/request/${route.params.id}/`)
        .then(response => {
            console.log('data', response.data)
            if (response.data.message === 'Request already fulfilled.') {
                toastStore.showToast(5000, 'Request already exists or Sent request to SELF', 'bg-red-300')
            } else {
                toastStore.showToast(5000, 'Request FULFILLED', 'bg-emerald-300')
            }
        })
        .catch(error => {
            console.log('error', error)
        })
}

function getFeed() {
    axios
        // .get(`/api/posts/profile/${this.route.params.id}`)
        .get(`/api/posts/profile/${route.params.id}`)
        .then(response => {
            posts.value = response.data.posts
            Object.assign(user, response.data.user)
            
            // user.value = response.data.user
            // console.log('user: ', user.value)
            // console.log('avatar: ', 'http://localhost:8000' + user.avatar)
        })
        .catch(error => {
            console.log('error', error)
        })
}

function logout() {
    userStore.removeToken()
    router.push('/login')
}

onMounted(() => { getFeed() })
// onUpdated(() => { getFeed() })
// onBeforeRouteUpdate(async (from, to) => {
//     getFeed() 
//     console.log('route updated')
// })

watch(route, () => {
    getFeed()
    console.log('route changed')
})

// onMounted(() => {
//     console.log('root: ', user_id)
// axios
//     // .get('/api/posts/profile/${$route.params.id}')
//     .get(`/api/posts/profile/${$route.params.id}`)
//     .then(response => {
//         posts.value = response.data.posts
//         user.value = response.data.user
//     })
//     .catch(error => {
//         console.log('error', error)
//     })
// })

</script>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <!-- <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full"> -->
                <img :src="user.get_avatar" class="mb-6 rounded-full">

                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="text-xs text-gray-500">{{
                        user.friends_count }} friends</RouterLink>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>

                <div class="mt-6">
                    <RouterLink v-if="userStore.user.id === user.id" to="/profile/edit"
                    class="inline-block mr-2 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg">EDIT</RouterLink>
                    <button v-if="userStore.user.id !== user.id" @click="sendFriendshipRequest"
                        class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg">Request Friendship</button>
                    <button v-else @click="logout"
                        class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg">Log Out</button>
                </div>

            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div v-if="userStore.user.id === user.id" class="bg-white border border-gray-200 rounded-lg">
                <FeedForm :user="user" :posts="posts" />
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <div class="mb-6 flex items-center justify-between">
                    <div class="flex items-center space-x-6">
                        <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">

                        <p><strong>Code With Stein</strong></p>
                    </div>

                    <p class="text-gray-600">18 minutes ago</p>
                </div>

                <img src="https://images.unsplash.com/photo-1661956602868-6ae368943878?ixlib=rb-4.0.3&amp;ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&amp;auto=format&amp;fit=crop&amp;w=2670&amp;q=80"
                    class="w-full rounded-lg">

                <!-- <div class="my-6 flex justify-between" v-for="post in posts" :key="post.id">
                    Hola, {{ post.body }}.
                </div> -->

                <div class="my-6 flex justify-between">
                    <div class="flex space-x-6">
                        <div class="flex items-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z">
                                </path>
                            </svg>

                            <span class="text-gray-500 text-xs">82 likes</span>
                        </div>

                        <div class="flex items-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
                                </path>
                            </svg>

                            <span class="text-gray-500 text-xs">0 comments</span>
                        </div>
                    </div>

                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
                            </path>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- <div v-if="userStore.user.id === user.id" class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" :key="post.id"> -->
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" :key="post.id">
                <FeedItem :post="post" />
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>
