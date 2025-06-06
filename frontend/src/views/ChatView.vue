<script setup>
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { onMounted, reactive, ref } from 'vue';

const body = ref('')
const conversations = ref([])
const activeConversation = reactive({})
const userstore = useUserStore()

function getMessages() {
    axios
        .get(`/api/chat/${activeConversation.id}`)
        .then(response => {
            // activeConversation = response.data
            Object.assign(activeConversation, response.data)
        })
        .catch(error => {
            console.log(error)
        })
}

function sendMessage() {
    axios
        .post(`/api/chat/${activeConversation.id}/send/`, {
            body: body.value
        }
        )
        .then(response => {
            activeConversation.messages.push(response.data)
            console.log(response.data)
        })
        .catch(err => {
            console.log(err)
        })

    body.value = ''
}

function setActiveConversation(id) {
    console.log('setActiveConversation', id)
}

onMounted(() => {
    axios
        .get(`/api/chat/`)
        .then(response => {
            conversations.value = response.data
            if (conversations.value.length) {
                // activeConversation = conversations[0].value, not work🚩
                Object.assign(activeConversation, conversations.value[0])
                // console.log(activeConversation.users)
                getMessages()
            }
        })
        .catch(error => {
            console.log(error)
        })
})
</script>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="space-y-4">
                    <div v-for="conversation in conversations" :key="conversation.id" @click="setActiveConversation(conversation.id)"
                        class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <!-- <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full"> -->
                            
                            <!-- <p class="text-xs"><strong>Code With Stein</strong></p> -->
                            <template v-for="user in conversation.users" :key="user.id">
                                <p class="text-xs font-bold" v-if="user.id !== userstore.user.id">
                                    <img :src="user.get_avatar" class="w-[40px] rounded-full">
                                    {{ user.name }}
                                </p>
                            </template>
                        </div>

                        <span class="text-xs text-gray-500">18 minutes ago</span>
                    </div>
                    <!-- 
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">

                            <p class="text-xs"><strong>Code With Stein</strong></p>
                        </div>

                        <span class="text-xs text-gray-500">18 minutes ago</span>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">

                            <p class="text-xs"><strong>Code With Stein</strong></p>
                        </div>

                        <span class="text-xs text-gray-500">18 minutes ago</span>
                    </div> -->
                </div>
            </div>
        </div>

        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg ">
                <div class="flex flex-col flex-grow p-4">
                    <template v-for="message in activeConversation.messages" :key="message.id">
                        <div v-if="message.sent_by.id == userstore.user.id"
                            class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                            <div>
                                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <!-- <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod.</p> -->
                                    <p class="text-sm">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ message.created_formatted }}
                                    ago</span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img :src="message.sent_by.get_avatar" class="w-[40px] rounded-full">
                            </div>
                        </div>

                        <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img :src="message.sent_by.get_avatar" class="w-[40px] rounded-full">
                            </div>
                            <div>
                                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                    <p class="text-sm">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ message.created_formatted }}
                                    ago</span>
                            </div>
                        </div>
                    </template>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg">
                <form @submit.prevent="sendMessage">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg resize-none"
                            placeholder="What do you want to say?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button href="#"
                            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Send</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>