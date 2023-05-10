<script>
    import copy from "copy-to-clipboard";
    import ImageWithAlt from "./imageWithAlt.svelte";
    import { toast } from '@zerodevx/svelte-toast'
    export let id;
    let title;
    let date;
    let titleText;
    let imgURL;
    let transcript;
    (async () => {
        const res = await fetch(`/fetchxkcd/${id}`);
        const json = await res.json();
        titleText = json.alt;
        title = json.title;
        date = json.day + "-" + json.month + "-" + json.year + " (M-D-Y)";
        imgURL = json.img;
        transcript = json.transcript;
    })();

    function copyLink() {
        const url = `https://xkcd.com/${id}`;
        copy(url);
        toast.push("Successfully copied to clipboard!", {
        theme: {
          "--toastBarBackground": "limegreen",
        },
      });
    }
</script>

<div class="text-left m-auto block mb-10">
    <h2 class="text-2xl p-0 text-black font-semibold">{title || "Loading title..."}</h2>
    <p class="text-gray-500 text-sm m-1 mt-0 inline-flex gap-1">
        <span>{date || "Loading date..."}</span>•<span
            on:click={copyLink}
            class="cursor-pointer underline">Copy to clipboard</span
        >•<a
            class="text-gray-500 underline"
            href={`https://explainxkcd.com/${id}`}
            target="_blank">explainxkcd.com</a
        >
    </p>
    <ImageWithAlt src={imgURL} alt={transcript}/>
    <img src={imgURL} class=" max-h-96" alt={transcript} />
    
    <p class="m-3 ml-0 text-black">{titleText || "Loading title text..."}</p>
</div>
