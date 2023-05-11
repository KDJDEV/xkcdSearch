<script>
    import ImagePlaceholder from "./ImagePlaceholder.svelte";
    export let src;
    export let alt = "";

    let loaded = false;

    function doneLoading() {
        loaded = true;
    }
</script>

<img {src} {alt} on:load={doneLoading} on:error={doneLoading} class="max-h-96" />
{#if !loaded}
<ImagePlaceholder />
{/if}
