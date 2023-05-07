<script>
    import { Accordion, AccordionItem } from "flowbite-svelte";
    export let mostRecentComicData;
    import { fade } from "svelte/transition";
</script>

<div>
    <h2 class="text-4xl mb-3 mt-5">FAQ</h2>
    <div class="text-left">
        <Accordion>
            <AccordionItem open>
                <span slot="header"
                    >Do you always have the most recent comics?</span
                >
                <p class="mb-2 text-gray-500 dark:text-gray-400">
                    There will be a delay of about 2 days after when a comic is
                    released before it is added to the database. This is
                    purposefully so that the <a href="https://explainxkcd.com">explainxkcd.com</a> page for the comic
                    can become more developed so that the AI can get a better
                    sense of each comic's intent.
                </p>
                {#if mostRecentComicData}
                    <p in:fade>The most recent comic in the database is #{mostRecentComicData.num}: {mostRecentComicData.safe_title}.</p>
                {/if}
            </AccordionItem>
            <AccordionItem>
                <span slot="header">How does the search work?</span>
                <p class="mb-2 text-gray-500 dark:text-gray-400">
                    Data about each comic, such as the title, transcript, explanation, etc. are gathered from <a href="https://xkcd.com">xkcd.com</a> and <a href="https://explainxkcd.com">explainxkcd.com</a>. This data is converted in <a href="https://platform.openai.com/docs/api-reference/embeddings">OpenAI's embeddings</a>, and then added to a vector database. When you make a search, your text is also converted to an embedding, which is then compared to each embedding in the database to find similar intent.
                </p>
            </AccordionItem>
        </Accordion>
    </div>
</div>
