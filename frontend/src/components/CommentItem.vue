<script setup>
import axios from 'axios';
// import { comment } from 'postcss';

// defineProps(['comment'])
defineProps({
    comment: Object
})

</script>

<template>
    <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-6">
            <img :src="comment.author.get_avatar" class="w-[40px] rounded-full">

            <p>
                <strong>
                    <RouterLink :to="{ name: 'profile', params: { 'id': comment.author.id } }">
                        {{ comment.author.name }}
                    </RouterLink>
                </strong>
            </p>
        </div>

        <p class="text-gray-600">{{ comment.created_formatted }} ago</p>
    </div>

    <p>
        {{ comment.body }}
    </p>
</template>