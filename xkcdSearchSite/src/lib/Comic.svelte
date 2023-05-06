<script>
    import { Toast } from "flowbite-svelte";
    import { fly } from "svelte/transition";
    import copy from 'copy-to-clipboard';
    
    export let id;
    let title;
    let date;
    let titleText;
    let imgURL;
    let transcript;
    (async () => {
        const res = await fetch(`http://127.0.0.1:5000/fetchxkcd/${id}`);
        const json = await res.json();
        titleText = json.alt;
        title = json.title;
        date = json.day + "-" + json.month + "-" + json.year + " (M-D-Y)";
        imgURL = json.img;
        transcript = json.transcript;
    })();

    let copiedNotification = false;
    function copyLink(){
        const url = `https://xkcd.com/${id}`;
        copy(url);
        if (!copiedNotification){
            copiedNotification = true;
            setTimeout(() => {
                copiedNotification = false;
            }, 3000);
        }
    }
</script>

<div class="text-left m-auto inline-block">
<h2 class="text-2xl p-0">{title}</h2>
<p class="text-gray-500 text-sm m-1 mt-0 inline-flex gap-1"><span>{date}</span>•<span on:click={copyLink} class="cursor-pointer underline">Copy to clipboard</span>•<a class="text-gray-500 underline" href={`https://explainxkcd.com/${id}`} target="_blank">explainxkcd.com</a></p>
<img src={imgURL} class=" max-h-96" alt={transcript}/>
<p class="m-3 ml-0">{titleText}</p>
</div>

{#if copiedNotification}
    <Toast transition={fly} params="{{x: 200, duration:250}}" color="green" class="mb-2 fixed top-2 right-2">
        <svelte:fragment slot="icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </svelte:fragment>
        Successfully copied to clipboard
    </Toast>
{/if}