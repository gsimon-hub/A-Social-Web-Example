<script setup>
import CommentItem from '@/components/CommentItem.vue';
import FeedItem from '@/components/FeedItem.vue';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import axios from 'axios';
import { onMounted, reactive, ref} from 'vue';
import { useRoute } from 'vue-router';

// const posts = ref([])
const post = reactive({
    id: null,
    comments: [],
})
const body = ref('')

// const post = reactive({})
const route = useRoute()

onMounted(() => {
    // console.log('Route ID: ', route.params.id)
    axios
        .get(`/api/posts/${route.params.id}/`)
        .then(response => {
            // posts.value = response.data
            Object.assign(post, response.data.post)
            // console.log('POST object: ', post.author)
        })
        .catch(error => {
            console.log('error', error)
        })
    })
    
function submitForm() {
    console.log('submitForm', body.value)
    axios
        .post(`/api/posts/${route.params.id}/comment/`, {
            'body': body.value
        })
        .then(response => {
            console.log('data', response.data)
            body.value = ''
        })
        .catch(error => {
            console.log('error', error)
        })
}

</script>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
       
        <div class="main-center col-span-3 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded-lg"  v-if="post.id">
                <FeedItem :post="post" />
            </div>

            <div v-for="comment in post.comments" :key="comment.id" class="p-4 ml-6 bg-white border border-gray-200 rounded-lg">
                <CommentItem :comment="comment"/>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg">
                <form method="post" @submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="What are you thinking about?"></textarea>
                    </div>
    
                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Comment</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>